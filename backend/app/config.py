import os
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB: str = os.getenv("MONGODB_DB", "meeting_ai")
USE_STUB: bool = os.getenv("USE_STUB", "1") == "1"
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_DEVICE: str = os.getenv("HUGGINGFACE_DEVICE", "cpu")

# Storage
UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "backend/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
