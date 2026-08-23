from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import AnalyticsEvent, Lead, LeadStage
from ..security import current_context
router=APIRouter(prefix="/analytics",tags=["analytics"])
@router.get("/overview")
def overview(ctx=Depends(current_context),db:Session=Depends(get_db)):
    wid=ctx["workspace_id"]
    total=db.query(func.count(Lead.id)).filter(Lead.workspace_id==wid).scalar() or 0
    won=db.query(func.count(Lead.id)).filter(Lead.workspace_id==wid,Lead.stage==LeadStage.won).scalar() or 0
    value=db.query(func.coalesce(func.sum(Lead.value_minor),0)).filter(Lead.workspace_id==wid,Lead.stage==LeadStage.won).scalar() or 0
    events=db.query(AnalyticsEvent.event_type,func.sum(AnalyticsEvent.value)).filter(AnalyticsEvent.workspace_id==wid).group_by(AnalyticsEvent.event_type).all()
    return {"leads":total,"won":won,"conversion":round(won/total,4) if total else 0,"revenue_minor":value,"events":{k:int(v or 0) for k,v in events}}
