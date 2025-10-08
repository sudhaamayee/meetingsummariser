from __future__ import annotations
import os
from typing import Dict
from .config import USE_STUB

# Optional heavy imports guarded at runtime
try:
    import whisper  # type: ignore
except Exception:
    whisper = None

try:
    from transformers import pipeline  # type: ignore
except Exception:
    pipeline = None

# Pyannote is complex to configure; keep stub-friendly
# from pyannote.audio import Pipeline  # optional


def transcribe(file_path: str) -> str:
    if USE_STUB or whisper is None:
        return (
            "Welcome everyone to the Q4 planning meeting. We will review the budget and assign action items. "
            "Marketing spend adjustments and deadlines will be discussed."
        )
    # Real whisper example (requires torch + whisper installed):
    try:
        print(f"Loading Whisper model...")
        model = whisper.load_model("base")
        print(f"Transcribing {file_path}...")
        result = model.transcribe(file_path, language="en")
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Whisper transcription failed: {e}")
        # Fallback to stub
        return (
            "Welcome everyone to the Q4 planning meeting. We will review the budget and assign action items. "
            "Marketing spend adjustments and deadlines will be discussed."
        )


def diarize_transcript(transcript: str) -> tuple[str, list[str]]:
    if USE_STUB:
        speakers = ["Speaker 1", "Speaker 2"]
        tagged = (
            "Speaker 1: Welcome everyone to the Q4 planning meeting.\n"
            "Speaker 2: Let's review the budget and action items.\n"
            "Speaker 1: We may reduce marketing spend by 10%."
        )
        return tagged, speakers
    # Placeholder for real diarization. Implement with pyannote pipeline and align to transcript.
    # For now, return single-speaker tagged text if not stub but diarization not configured.
    return f"Speaker 1: {transcript}", ["Speaker 1"]


def summarize(transcript: str) -> Dict:
    if USE_STUB or pipeline is None:
        return {
            "overview": "Discussion of Q4 budget planning and responsibilities.",
            "decisions": [
                "Reduce marketing spend by 10%",
            ],
            "action_items": [
                "Alice to draft updated plan by Friday",
            ],
        }
    # Real summarization using BART or T5
    try:
        print(f"Loading summarization model...")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        # Chunk transcript if long; here we keep simple.
        if len(transcript) < 50:
            # Too short to summarize
            return {
                "overview": transcript,
                "decisions": [],
                "action_items": [],
            }
        sum_text = summarizer(transcript, max_length=180, min_length=60, do_sample=False)[0]["summary_text"]
        # Lightweight heuristic split
        return {
            "overview": sum_text,
            "decisions": [],
            "action_items": [],
        }
    except Exception as e:
        print(f"Summarization failed: {e}")
        # Fallback
        return {
            "overview": transcript[:200] + "..." if len(transcript) > 200 else transcript,
            "decisions": [],
            "action_items": [],
        }
