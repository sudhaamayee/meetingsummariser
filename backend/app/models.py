from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        return ObjectId(str(v))

class Meeting(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    filename: str
    transcript: str
    speakers: List[str] = []
    summary: dict
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True

class MeetingCreate(BaseModel):
    filename: str
    transcript: str
    speakers: List[str] = []
    summary: dict

class MeetingOut(BaseModel):
    id: str = Field(alias="_id")
    filename: str
    transcript: str
    speakers: List[str]
    summary: dict
    createdAt: datetime
