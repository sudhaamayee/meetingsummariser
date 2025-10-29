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
        "https://meetingsummariserr.netlify.app",  # Production frontend
        "http://localhost:5173",                   # Local development
        "http://localhost:3000"                    # Common React dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
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

        # Generate a temporary ID for immediate response
        temp_id = "temp_" + str(abs(hash(file.filename + str(datetime.utcnow()))))[:12]
        
        # Prepare the document with temporary ID
        doc = MeetingCreate(
            filename=file.filename,
            transcript=tagged_transcript,
            speakers=speakers,
            summary=summary,
            temp_id=temp_id,  # Store the temp_id for later lookup
            createdAt=datetime.utcnow(),
            status="processing"
        ).model_dump()

        # Try to save to MongoDB
        db = await get_db()
        try:
            res = await db.meetings.insert_one(doc)
            doc["_id"] = str(res.inserted_id)  # Add string ID for response
            doc["temp_id"] = temp_id  # Ensure temp_id is included in the response
            logger.info(f"Successfully saved to database with ID: {doc['_id']}")
            return doc
        except Exception as e:
            logger.warning(f"Failed to save to database: {e}")
            # Return result with temp_id even if DB save fails
            return {
                "_id": temp_id,
                "temp_id": temp_id,
                "filename": file.filename,
                "transcript": tagged_transcript,
                "speakers": speakers,
                "summary": summary,
                "createdAt": datetime.utcnow().isoformat(),
                "status": "temporary"
            }
    except Exception as e:
        logger.error(f"Upload processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/summary/{id}")
async def get_summary(id: str):
    db = await get_db()
    
    # First check if it's a temporary ID (starts with 'temp_')
    if id.startswith('temp_'):
        # Look for the document with this temp_id
        doc = await db.meetings.find_one({"temp_id": id})
        if not doc:
            raise HTTPException(status_code=404, detail="Temporary summary not found. The summary may have expired or already been processed.")
    else:
        # Handle MongoDB ObjectId
        try:
            oid = ObjectId(id)
            doc = await db.meetings.find_one({"_id": oid})
            if not doc:
                raise HTTPException(status_code=404, detail="Summary not found")
        except Exception as e:
            logger.error(f"Error fetching summary: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid ID format")
    
    # Convert ObjectId to string for JSON serialization
    doc["_id"] = str(doc["_id"])
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
