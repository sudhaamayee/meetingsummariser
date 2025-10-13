"""
Quick script to check the current backend configuration
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

try:
    from app.config import USE_STUB, UPLOAD_DIR, MONGODB_URI
    
    print("=" * 60)
    print("Current Backend Configuration")
    print("=" * 60)
    print(f"\nUSE_STUB: {USE_STUB}")
    print(f"UPLOAD_DIR: {UPLOAD_DIR}")
    print(f"MONGODB_URI: {MONGODB_URI}")
    
    print("\n" + "=" * 60)
    print("AI Dependencies Check")
    print("=" * 60)
    
    # Check for whisper
    try:
        import whisper
        print("✓ Whisper: INSTALLED")
    except ImportError:
        print("✗ Whisper: NOT INSTALLED")
        if not USE_STUB:
            print("  ⚠ WARNING: USE_STUB=0 but Whisper not installed!")
            print("  Install with: pip install openai-whisper torch")
    
    # Check for transformers
    try:
        import transformers
        print("✓ Transformers: INSTALLED")
    except ImportError:
        print("✗ Transformers: NOT INSTALLED")
        if not USE_STUB:
            print("  ⚠ WARNING: USE_STUB=0 but Transformers not installed!")
            print("  Install with: pip install transformers sentencepiece")
    
    # Check for torch
    try:
        import torch
        print(f"✓ PyTorch: INSTALLED (version {torch.__version__})")
    except ImportError:
        print("✗ PyTorch: NOT INSTALLED")
        if not USE_STUB:
            print("  ⚠ WARNING: USE_STUB=0 but PyTorch not installed!")
            print("  Install with: pip install torch")
    
    print("\n" + "=" * 60)
    print("Status Summary")
    print("=" * 60)
    
    if USE_STUB:
        print("\n✓ STUB MODE ENABLED")
        print("  All uploads will return static test data")
        print("  No AI dependencies required")
    else:
        print("\n✓ REAL AI MODE ENABLED")
        # Check if all dependencies are installed
        try:
            import whisper
            import transformers
            import torch
            print("  ✓ All required dependencies installed")
            print("  Uploads will be processed with real AI models")
        except ImportError as e:
            print("  ✗ MISSING DEPENDENCIES!")
            print("  The server will fail when processing uploads")
            print("\n  To fix, either:")
            print("  1. Install dependencies: pip install torch openai-whisper transformers sentencepiece")
            print("  2. Enable stub mode: Set USE_STUB=1 in backend/.env")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"Error loading configuration: {e}")
    print("\nMake sure you're running this from the project root:")
    print("  python backend/check_config.py")
