from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand, ContentItem
from ..schemas import ContentIn
from ..security import current_context
router=APIRouter(prefix="/content",tags=["content"])
@router.get("")
def list_content(ctx=Depends(current_context),db:Session=Depends(get_db)):
    ids=[b.id for b in db.query(Brand).filter_by(workspace_id=ctx["workspace_id"]).all()]
    return db.query(ContentItem).filter(ContentItem.brand_id.in_(ids)).order_by(ContentItem.created_at.desc()).limit(100).all() if ids else []
@router.post("")
def create_content(data:ContentIn,ctx=Depends(current_context),db:Session=Depends(get_db)):
    b=db.query(Brand).filter_by(id=data.brand_id,workspace_id=ctx["workspace_id"]).first()
    if not b: raise HTTPException(404,"Brand not found")
    item=ContentItem(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
