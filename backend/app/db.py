from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGODB_URI, MONGODB_DB

_client: AsyncIOMotorClient | None = None
_db = None

async def get_db():
    global _client, _db
    if _client is None:
        _client = AsyncIOMotorClient(MONGODB_URI)
        _db = _client[MONGODB_DB]
    return _db
