"""
Setup script to configure the backend .env file
Run this to enable real AI processing instead of stub data
"""
import os
from pathlib import Path

def setup_env():
    backend_dir = Path(__file__).parent
    env_file = backend_dir / ".env"
    env_example = backend_dir / ".env.example"
    
    print("=" * 60)
    print("Meeting AI Backend Setup")
    print("=" * 60)
    
    # Check if .env exists
    if env_file.exists():
        print(f"\n✓ Found existing .env file at: {env_file}")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'USE_STUB=1' in content:
                print("⚠ WARNING: USE_STUB is currently set to 1 (stub mode)")
                print("  This means uploads will return static test data")
            elif 'USE_STUB=0' in content:
                print("✓ USE_STUB is set to 0 (real AI processing enabled)")
            else:
                print("⚠ USE_STUB not found in .env file")
    else:
        print(f"\n✗ No .env file found")
        if env_example.exists():
            print(f"  Creating .env from .env.example...")
            with open(env_example, 'r') as src:
                with open(env_file, 'w') as dst:
                    dst.write(src.read())
            print(f"✓ Created .env file")
        else:
            print(f"  Creating default .env file...")
            default_env = """# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=meeting_ai

# AI Processing Mode
# Set to "0" to enable real AI processing (requires installing heavy dependencies)
# Set to "1" to use stub/mock data for testing
USE_STUB=0

# HuggingFace Device (cpu or cuda)
HUGGINGFACE_DEVICE=cpu

# Upload Directory
UPLOAD_DIR=backend/uploads
"""
            with open(env_file, 'w') as f:
                f.write(default_env)
            print(f"✓ Created default .env file")
    
    print("\n" + "=" * 60)
    print("Configuration Options:")
    print("=" * 60)
    
    choice = input("\nDo you want to enable REAL AI processing? (y/n): ").strip().lower()
    
    if choice == 'y':
        # Update .env to disable stub mode
        with open(env_file, 'r') as f:
            content = f.read()
        
        content = content.replace('USE_STUB=1', 'USE_STUB=0')
        if 'USE_STUB=0' not in content and 'USE_STUB=' not in content:
            content += '\nUSE_STUB=0\n'
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("\n✓ Updated .env: USE_STUB=0")
        print("\n" + "=" * 60)
        print("IMPORTANT: Install AI Dependencies")
        print("=" * 60)
        print("\nTo use real AI processing, you need to install:")
        print("  pip install torch openai-whisper transformers sentencepiece")
        print("\nNote: These packages are large (~2-3GB download)")
        print("First transcription will download AI models (~1-2GB)")
        
        install = input("\nInstall dependencies now? (y/n): ").strip().lower()
        if install == 'y':
            import subprocess
            print("\nInstalling dependencies (this may take several minutes)...")
            try:
                subprocess.check_call([
                    'pip', 'install', 
                    'torch', 'openai-whisper', 'transformers', 'sentencepiece'
                ])
                print("\n✓ Dependencies installed successfully!")
            except Exception as e:
                print(f"\n✗ Installation failed: {e}")
                print("  Please install manually with:")
                print("  pip install torch openai-whisper transformers sentencepiece")
    else:
        # Keep stub mode
        with open(env_file, 'r') as f:
            content = f.read()
        
        content = content.replace('USE_STUB=0', 'USE_STUB=1')
        if 'USE_STUB=1' not in content and 'USE_STUB=' not in content:
            content += '\nUSE_STUB=1\n'
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("\n✓ Updated .env: USE_STUB=1 (stub mode)")
        print("  All uploads will return consistent test data")
        print("  No AI dependencies needed")
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start the backend server:")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend")
    print("\n2. Check the startup logs for:")
    print("   - 'USE_STUB mode: True/False'")
    print("   - 'Whisper module loaded successfully' (if USE_STUB=0)")
    print("\n3. Upload a video and check if it processes correctly")
    print("=" * 60)

if __name__ == "__main__":
    setup_env()
