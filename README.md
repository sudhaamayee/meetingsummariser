# AI-Based Meeting Transcription and Summarization Tool

A minimal full-stack app to upload meeting audio and get:
- Transcript with speaker tags
- Concise summary: overview, decisions, action items

Stack
- Frontend: React (Vite) + TailwindCSS
- Backend: FastAPI (Python)
- DB: MongoDB Atlas (Motor)
- AI Pipeline: Whisper (transcription), Pyannote (speaker diarization), HuggingFace (summarization)

Quick Start

Backend
1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Set up environment variables:**
   - Copy `backend/.env.example` to `backend/.env` and fill values
   - (Optional) Keep `USE_STUB=1` to run without heavy AI models

3. **Create virtual environment and install dependencies:**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment (Windows)
   .venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Run the backend server:**
   ```bash
   # From the backend directory
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Or from the project root:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend
   ```

5. **Verify the server is running:**
   - Open http://localhost:8000/docs in your browser
   - You should see the FastAPI interactive documentation

Frontend
1. From `frontend/`:
   - `npm install`
   - `npm run dev`
2. Set `VITE_API_BASE` in `frontend/.env` (default: http://localhost:8000)

Deployment
- Frontend: Netlify/Vercel
- Backend: Render/Railway
- DB: MongoDB Atlas

Environment Variables
- Backend: see `backend/.env.example`
- Frontend: see `frontend/.env.example`

Notes
- Stub mode returns deterministic fake outputs suitable for development.
- Replace stub by setting `USE_STUB=0` and installing optional heavy packages (see comments in `backend/requirements.txt`).

## Troubleshooting

### Getting Static/Stub Data After Upload

If you're still getting static data after uploading a video, check the following:

1. **Check USE_STUB setting in backend/.env**
   ```bash
   # In backend/.env, set:
   USE_STUB=0
   ```

2. **Install AI dependencies** (required when USE_STUB=0)
   ```bash
   # Activate your virtual environment first
   .venv\Scripts\activate  # Windows
   
   # Install the heavy AI dependencies
   pip install torch openai-whisper transformers sentencepiece
   ```

3. **Restart the backend server**
   ```bash
   # Stop the current server (Ctrl+C) and restart:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend
   ```

4. **Check the logs** - The server will now show detailed logs:
   - "USE_STUB mode: False" on startup
   - "Loading Whisper model..." during processing
   - "Transcription completed: X characters"

### If You Want to Keep Using Stub Mode

If you prefer to use stub mode for testing (no AI dependencies needed):
1. Set `USE_STUB=1` in `backend/.env`
2. The system will return consistent test data for all uploads

### Performance Notes

- First upload with real AI will be slow (downloading models ~1-2GB)
- Subsequent uploads will be faster (models cached)
- Processing time depends on audio length (~1-2 min per 10 min of audio)
