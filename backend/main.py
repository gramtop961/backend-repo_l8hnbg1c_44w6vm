from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List

from database import create_document, get_documents

app = FastAPI(title="TGP Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.get("/test")
async def test():
    return {"status": "ok"}

# Public getters
@app.get("/bio", response_model=List[dict])
async def get_bio():
    return await get_documents("bio", {}, 10)

@app.get("/social_links", response_model=List[dict])
async def get_social_links():
    return await get_documents("sociallink", {}, 100)

@app.get("/skills", response_model=List[dict])
async def get_skills():
    return await get_documents("skill", {}, 500)

@app.get("/projects", response_model=List[dict])
async def get_projects():
    return await get_documents("project", {}, 100)

@app.get("/certifications", response_model=List[dict])
async def get_certifications():
    return await get_documents("certification", {}, 200)

@app.get("/achievements", response_model=List[dict])
async def get_achievements():
    return await get_documents("achievement", {}, 200)

@app.get("/timeline", response_model=List[dict])
async def get_timeline():
    return await get_documents("timeline", {}, 200)

# Simple create endpoints (Admin would normally auth; placeholder here)
@app.post("/admin/create/{collection}")
async def admin_create(collection: str, payload: dict):
    if collection not in {"bio","sociallink","skill","project","certification","achievement","timeline","adminuser"}:
        raise HTTPException(status_code=400, detail="Invalid collection")
    doc = await create_document(collection, payload)
    return doc

@app.post("/contact")
async def contact(msg: ContactMessage):
    # Store message; in a real app, trigger email via provider/edge function
    doc = await create_document("contact", msg.model_dump())
    return {"ok": True, "id": doc.get("_id")}
