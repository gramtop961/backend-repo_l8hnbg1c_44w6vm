from typing import Any, Dict, Optional
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel

MONGO_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(MONGO_URL)
        _db = _client[DB_NAME]
    return _db

class TimeStampedModel(BaseModel):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

async def create_document(collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    from datetime import datetime
    now = datetime.utcnow().isoformat()
    data["created_at"] = now
    data["updated_at"] = now
    res = await db[collection].insert_one(data)
    return {"_id": str(res.inserted_id), **data}

async def get_documents(collection: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50):
    db = await get_db()
    cursor = db[collection].find(filter_dict or {}).limit(limit)
    docs = []
    async for d in cursor:
        d["_id"] = str(d["_id"])  # convert ObjectId
        docs.append(d)
    return docs
