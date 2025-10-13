from __future__ import annotations
import os
import logging
import re
from typing import Dict, List
from .config import USE_STUB

logger = logging.getLogger(__name__)

# Optional heavy imports guarded at runtime
try:
    import whisper  # type: ignore
    logger.info("Whisper module loaded successfully")
except Exception as e:
    whisper = None
    logger.warning(f"Whisper not available: {e}")

try:
    from transformers import pipeline  # type: ignore
    logger.info("Transformers module loaded successfully")
except Exception as e:
    pipeline = None
    logger.warning(f"Transformers not available: {e}")

# Pyannote is complex to configure; keep stub-friendly
# from pyannote.audio import Pipeline  # optional


def transcribe(file_path: str) -> str:
    """Transcribe audio file to text using Whisper or return stub data."""
    if USE_STUB:
        logger.info("Using STUB mode for transcription")
        return (
            "Welcome everyone to the Q4 planning meeting. We will review the budget and assign action items. "
            "Marketing spend adjustments and deadlines will be discussed."
        )
    
    if whisper is None:
        logger.error("Whisper not installed. Install with: pip install openai-whisper torch")
        raise RuntimeError("Whisper not available. Please install dependencies or set USE_STUB=1")
    
    # Real whisper transcription
    try:
        logger.info(f"Loading Whisper model...")
        model = whisper.load_model("base")
        logger.info(f"Transcribing {file_path}...")
        result = model.transcribe(file_path, language="en", fp16=False)
        transcript = result.get("text", "").strip()
        logger.info(f"Transcription completed: {len(transcript)} characters")
        return transcript
    except FileNotFoundError as e:
        logger.error(f"FFmpeg not found: {e}")
        raise RuntimeError(
            "FFmpeg is required but not found. "
            "Install it from: https://www.gyan.dev/ffmpeg/builds/ "
            "Or use Chocolatey: choco install ffmpeg "
            "Or set USE_STUB=1 in .env to use test data"
        )
    except Exception as e:
        logger.error(f"Whisper transcription failed: {e}")
        raise RuntimeError(f"Transcription failed: {str(e)}")


def diarize_transcript(transcript: str) -> tuple[str, list[str]]:
    """Add speaker labels to transcript. Uses stub mode or simple single-speaker format."""
    if USE_STUB:
        logger.info("Using STUB mode for diarization")
        speakers = ["Speaker 1", "Speaker 2"]
        tagged = (
            "Speaker 1: Welcome everyone to the Q4 planning meeting.\n"
            "Speaker 2: Let's review the budget and action items.\n"
            "Speaker 1: We may reduce marketing spend by 10%."
        )
        return tagged, speakers
    
    # Placeholder for real diarization. Implement with pyannote pipeline and align to transcript.
    # For now, return single-speaker tagged text if not stub but diarization not configured.
    logger.info("Using simple single-speaker diarization (pyannote not configured)")
    return f"Speaker 1: {transcript}", ["Speaker 1"]


def extract_action_items(transcript: str) -> List[str]:
    """Extract action items from transcript using keyword patterns."""
    action_items = []
    
    # Patterns that indicate action items
    action_patterns = [
        r"(?:will|should|need to|have to|must|going to|plan to)\s+([^.!?]+)",
        r"(?:action item|task|todo|to-do):\s*([^.!?]+)",
        r"([A-Z][a-z]+)\s+(?:will|should|needs to|has to)\s+([^.!?]+)",
        r"(?:implement|develop|create|build|design|prepare|draft)\s+([^.!?]+)",
    ]
    
    for pattern in action_patterns:
        matches = re.finditer(pattern, transcript, re.IGNORECASE)
        for match in matches:
            item = match.group(0).strip()
            if len(item) > 20 and len(item) < 150:  # Reasonable length
                # Clean up the item
                item = item.capitalize()
                if not item.endswith('.'):
                    item += '.'
                if item not in action_items:
                    action_items.append(item)
    
    # Limit to top 5 most relevant
    return action_items[:5] if action_items else ["No specific action items identified"]


def extract_decisions(transcript: str) -> List[str]:
    """Extract decisions from transcript using keyword patterns."""
    decisions = []
    
    # Patterns that indicate decisions
    decision_patterns = [
        r"(?:decided|agreed|determined|concluded)\s+(?:to|that)\s+([^.!?]+)",
        r"(?:decision|choice|resolution):\s*([^.!?]+)",
        r"(?:we will|we'll|team will)\s+([^.!?]+)",
        r"(?:approved|selected|chosen)\s+([^.!?]+)",
    ]
    
    for pattern in decision_patterns:
        matches = re.finditer(pattern, transcript, re.IGNORECASE)
        for match in matches:
            item = match.group(0).strip()
            if len(item) > 20 and len(item) < 150:  # Reasonable length
                # Clean up the item
                item = item.capitalize()
                if not item.endswith('.'):
                    item += '.'
                if item not in decisions:
                    decisions.append(item)
    
    # Limit to top 5 most relevant
    return decisions[:5] if decisions else ["No specific decisions identified"]


def summarize(transcript: str) -> Dict:
    """Generate summary with overview, decisions, and action items."""
    if USE_STUB:
        logger.info("Using STUB mode for summarization")
        return {
            "overview": "Discussion of Q4 budget planning and responsibilities.",
            "decisions": [
                "Reduce marketing spend by 10%",
            ],
            "action_items": [
                "Alice to draft updated plan by Friday",
            ],
        }
    
    # Extract decisions and action items from transcript
    logger.info("Extracting decisions and action items...")
    decisions = extract_decisions(transcript)
    action_items = extract_action_items(transcript)
    
    if pipeline is None:
        logger.warning("Transformers not installed. Using rule-based extraction.")
        # Create a better overview from first few sentences
        sentences = transcript.split('.')[:3]
        overview = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
        return {
            "overview": overview if len(overview) < 500 else overview[:500] + "...",
            "decisions": decisions,
            "action_items": action_items,
        }
    
    # Real summarization using BART or T5
    try:
        logger.info(f"Loading summarization model...")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        
        # Chunk transcript if long; here we keep simple.
        if len(transcript) < 50:
            logger.warning("Transcript too short to summarize")
            return {
                "overview": transcript,
                "decisions": decisions,
                "action_items": action_items,
            }
        
        logger.info(f"Summarizing transcript ({len(transcript)} characters)...")
        # Limit input length for BART
        max_input = 1024
        transcript_chunk = transcript[:max_input] if len(transcript) > max_input else transcript
        sum_text = summarizer(transcript_chunk, max_length=180, min_length=60, do_sample=False)[0]["summary_text"]
        logger.info(f"Summarization completed")
        
        return {
            "overview": sum_text,
            "decisions": decisions,
            "action_items": action_items,
        }
    except Exception as e:
        logger.warning(f"Summarization failed: {e}. Using rule-based extraction.")
        # Create overview from first few sentences
        sentences = transcript.split('.')[:3]
        overview = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
        return {
            "overview": overview if len(overview) < 500 else overview[:500] + "...",
            "decisions": decisions,
            "action_items": action_items,
        }
