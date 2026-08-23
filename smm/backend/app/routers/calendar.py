from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand, ContentItem, ContentStatus
from ..schemas import ContentIn
from ..security import current_context
router=APIRouter(prefix="/calendar",tags=["calendar"])
@router.get("")
def calendar(days:int=30,ctx=Depends(current_context),db:Session=Depends(get_db)):
    ids=[x.id for x in db.query(Brand).filter_by(workspace_id=ctx["workspace_id"]).all()]
    end=datetime.utcnow()+timedelta(days=min(days,90))
    return db.query(ContentItem).filter(ContentItem.brand_id.in_(ids),ContentItem.scheduled_at<=end).order_by(ContentItem.scheduled_at).all() if ids else []
@router.post("")
def schedule(data:ContentIn,ctx=Depends(current_context),db:Session=Depends(get_db)):
    b=db.query(Brand).filter_by(id=data.brand_id,workspace_id=ctx["workspace_id"]).first()
    if not b: raise HTTPException(404,"Brand not found")
    item=ContentItem(**data.model_dump(),status=ContentStatus.scheduled if data.scheduled_at else ContentStatus.draft)
    db.add(item); db.commit(); db.refresh(item); return item
