from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand,ContentItem
from ..security import current_context
from ..ai import generate
router=APIRouter(prefix="/ai-studio",tags=["ai-studio"])
class GenerateRequest(BaseModel):
    brand_id:str
    brief:str=Field(min_length=3,max_length=5000)
    networks:list[str]=[]
    save_draft:bool=True
@router.post("/generate")
async def create(req:GenerateRequest,ctx=Depends(current_context),db:Session=Depends(get_db)):
    brand=db.query(Brand).filter_by(id=req.brand_id,workspace_id=ctx["workspace_id"]).first()
    if not brand: raise HTTPException(404,"Brand not found")
    channels=req.networks or ["telegram","vk","instagram"]
    out=await generate(db,brand,f"Create a channel-adaptable content package for: {req.brief}. Channels: {', '.join(channels)}. Return concise copy, hook, CTA, and short-video concept.","content")
    content_id=None
    if req.save_draft:
        item=ContentItem(brand_id=brand.id,title=req.brief[:120],body=out["text"],networks=channels,ai_generated=True)
        db.add(item); db.commit(); db.refresh(item); content_id=item.id
    return {**out,"content_id":content_id,"networks":channels}
