from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Lead
from ..schemas import LeadIn
from ..security import current_context
router=APIRouter(prefix="/leads",tags=["leads"])
@router.get("")
def list_leads(ctx=Depends(current_context),db:Session=Depends(get_db)):
    return db.query(Lead).filter_by(workspace_id=ctx["workspace_id"]).order_by(Lead.created_at.desc()).limit(200).all()
@router.post("")
def create_lead(data:LeadIn,ctx=Depends(current_context),db:Session=Depends(get_db)):
    lead=Lead(workspace_id=ctx["workspace_id"],**data.model_dump()); db.add(lead); db.commit(); db.refresh(lead); return lead
