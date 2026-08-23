from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: str = ""
    workspace_name: str = "My workspace"
class LoginIn(BaseModel):
    email: EmailStr
    password: str
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    workspace_id: str
class BrandIn(BaseModel):
    name: str
    description: str = ""
    tone_of_voice: str = ""
    target_audience: str = ""
class KnowledgeIn(BaseModel):
    title: str
    content: str
    kind: str = "note"
    tags: list[str] = []
class ContentIn(BaseModel):
    brand_id: str
    title: str = ""
    body: str
    networks: list[str] = []
    scheduled_at: datetime | None = None
class LeadIn(BaseModel):
    brand_id: str | None = None
    name: str = ""
    source: str
    source_detail: str = ""
    score: int = 0
class AutopilotRequest(BaseModel):
    brand_id: str
    objective: str = "growth"
    horizon_days: int = 7
    channels: list[str] = []
