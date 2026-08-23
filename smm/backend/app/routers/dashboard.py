from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand, ContentItem, ContentStatus, Conversation, Lead, LeadStage
from ..security import current_context
router=APIRouter(tags=["dashboard"])
@router.get("/dashboard")
def dashboard(ctx=Depends(current_context),db:Session=Depends(get_db)):
    wid=ctx["workspace_id"]; brand_ids=[b.id for b in db.query(Brand).filter_by(workspace_id=wid).all()]
    scheduled=db.query(func.count(ContentItem.id)).filter(ContentItem.brand_id.in_(brand_ids),ContentItem.status==ContentStatus.scheduled).scalar() if brand_ids else 0
    unread=db.query(func.coalesce(func.sum(Conversation.unread_count),0)).filter(Conversation.brand_id.in_(brand_ids)).scalar() if brand_ids else 0
    leads=db.query(func.count(Lead.id)).filter(Lead.workspace_id==wid,Lead.stage==LeadStage.new).scalar() or 0
    return {"brands":len(brand_ids),"scheduled":scheduled or 0,"unread_inbox":int(unread or 0),"new_leads":leads,"autopilot":"ready"}
