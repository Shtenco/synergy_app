from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand, BrandKnowledge
from ..schemas import BrandIn, KnowledgeIn
from ..security import current_context
router=APIRouter(prefix="/brands",tags=["brands"])
@router.get("")
def list_brands(ctx=Depends(current_context),db:Session=Depends(get_db)):
    return db.query(Brand).filter_by(workspace_id=ctx["workspace_id"]).all()
@router.post("")
def create_brand(data:BrandIn,ctx=Depends(current_context),db:Session=Depends(get_db)):
    b=Brand(workspace_id=ctx["workspace_id"],**data.model_dump()); db.add(b); db.commit(); db.refresh(b); return b
@router.post("/{brand_id}/knowledge")
def add_knowledge(brand_id:str,data:KnowledgeIn,ctx=Depends(current_context),db:Session=Depends(get_db)):
    b=db.query(Brand).filter_by(id=brand_id,workspace_id=ctx["workspace_id"]).first()
    if not b: raise HTTPException(404,"Brand not found")
    k=BrandKnowledge(brand_id=b.id,**data.model_dump()); db.add(k); db.commit(); db.refresh(k); return k
@router.get("/{brand_id}/knowledge")
def knowledge(brand_id:str,ctx=Depends(current_context),db:Session=Depends(get_db)):
    b=db.query(Brand).filter_by(id=brand_id,workspace_id=ctx["workspace_id"]).first()
    if not b: raise HTTPException(404,"Brand not found")
    return db.query(BrandKnowledge).filter_by(brand_id=brand_id).all()
