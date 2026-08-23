from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal
router=APIRouter(prefix="/content", tags=["content"])
class ContentDraft(BaseModel):
    brand_id:str
    title:str
    body:str
    channels:list[Literal["vk","telegram","instagram","facebook","whatsapp","ok","zen"]]=[]
@router.post("")
def create_content(draft:ContentDraft): return {"id":"cnt_demo_001","status":"draft",**draft.model_dump()}
@router.get("")
def list_content(): return [{"id":"cnt_demo_001","title":"Первый AI-пост","status":"draft"}]
