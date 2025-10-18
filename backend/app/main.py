from __future__ import annotations
import os
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from .db import get_db
from .models import Meeting, MeetingCreate
from .ai import transcribe, diarize_transcript, summarize
from .config import UPLOAD_DIR, USE_STUB
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Meeting AI API")

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting Meeting AI API")
    logger.info(f"USE_STUB mode: {USE_STUB}")
    logger.info(f"Upload directory: {UPLOAD_DIR}")

# Dev CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins
        "https://meetingsummarise.netlify.app",  # Your Netlify domain
        "http://localhost:5173",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".mp3", ".wav", ".mp4")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    logger.info(f"Received upload request for file: {file.filename}")
    
    try:
        # Save temp file
        dest_path = os.path.join(UPLOAD_DIR, file.filename)
        logger.info(f"Saving file to: {dest_path}")
        with open(dest_path, "wb") as out:
            shutil.copyfileobj(file.file, out)
        
        file_size = os.path.getsize(dest_path)
        logger.info(f"File saved successfully ({file_size} bytes)")

        # AI pipeline
        logger.info("Starting transcription...")
        raw_transcript = transcribe(dest_path)
        
        logger.info("Starting diarization...")
        tagged_transcript, speakers = diarize_transcript(raw_transcript)
        
        logger.info("Starting summarization...")
        summary = summarize(tagged_transcript)

        doc = MeetingCreate(
            filename=file.filename,
            transcript=tagged_transcript,
            speakers=speakers,
            summary=summary,
        ).model_dump()

        # Try to save to MongoDB
        db = await get_db()
        try:
            res = await db.meetings.insert_one(doc)
            saved = await db.meetings.find_one({"_id": res.inserted_id})
            saved["_id"] = str(saved["_id"])  # serialize
            logger.info(f"Meeting saved to database with ID: {saved['_id']}")
            return saved
        except Exception as db_error:
            logger.warning(f"MongoDB save failed: {db_error}. Returning result without persistence.")
            # Return result without saving to DB
            doc["_id"] = "temp_" + str(abs(hash(file.filename + str(datetime.utcnow()))))[:12]
            doc["createdAt"] = datetime.utcnow().isoformat()
            return doc
    except Exception as e:
        logger.error(f"Upload processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/summary/{id}")
async def get_summary(id: str):
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid id")

    db = await get_db()
    doc = await db.meetings.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    doc["_id"] = str(doc["_id"])  # serialize
    return doc

@app.get("/history")
async def history():
    db = await get_db()
    cursor = db.meetings.find({}, {"transcript": 0})  # omit large field for list
    items = []
    async for d in cursor:
        d["_id"] = str(d["_id"])  # serialize
        items.append(d)
    return {"items": items}
