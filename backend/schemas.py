from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

# Each Pydantic model corresponds to a Mongo collection with the lowercased name

class Bio(BaseModel):
    name: str
    headline: str
    summary: str
    avatar_url: Optional[HttpUrl] = None

class SocialLink(BaseModel):
    platform: str
    url: HttpUrl
    icon: Optional[str] = None

class Skill(BaseModel):
    category: str  # Frontend, Backend, AI, Tools, Cloud
    name: str
    level: int = Field(ge=1, le=10)
    description: Optional[str] = None
    tags: List[str] = []

class Project(BaseModel):
    title: str
    description: str
    tags: List[str] = []
    github: Optional[HttpUrl] = None
    demo: Optional[HttpUrl] = None
    media_url: Optional[HttpUrl] = None
    ai_summary: Optional[str] = None

class Certification(BaseModel):
    title: str
    issuer: str
    year: int
    image_url: Optional[HttpUrl] = None
    category: Optional[str] = None
    caption: Optional[str] = None

class Achievement(BaseModel):
    title: str
    event: Optional[str] = None
    year: int
    description: Optional[str] = None
    badge_url: Optional[HttpUrl] = None

class Timeline(BaseModel):
    kind: str  # Education, Hackathon, Work, Achievement
    title: str
    org: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    details: Optional[str] = None

class AdminUser(BaseModel):
    email: str
    role: str = "admin"
