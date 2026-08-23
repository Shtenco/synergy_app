from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand, BrandKnowledge
from ..schemas import AutopilotRequest
from ..security import current_context
router=APIRouter(prefix="/autopilot",tags=["autopilot"])
@router.post("/plan")
def plan(data:AutopilotRequest,ctx=Depends(current_context),db:Session=Depends(get_db)):
    b=db.query(Brand).filter_by(id=data.brand_id,workspace_id=ctx["workspace_id"]).first()
    if not b: raise HTTPException(404,"Brand not found")
    knowledge=db.query(BrandKnowledge).filter_by(brand_id=b.id).all()
    channels=data.channels or ["telegram","vk","instagram"]
    themes=[k.title for k in knowledge[:5]] or ["экспертность","кейс","продукт","вовлечение","закулисье"]
    cadence=max(1,min(data.horizon_days,14))
    return {"brand_id":b.id,"objective":data.objective,"strategy":{"tone":b.tone_of_voice,"audience":b.target_audience,"channels":channels},"content_plan":[{"day":i+1,"theme":themes[i%len(themes)],"format":"short-form","channels":channels} for i in range(cadence)],"guardrails":["human approval before publishing","use only connected brand accounts","respect channel messaging and rate-limit policies"]}
