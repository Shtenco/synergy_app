from fastapi import APIRouter
router=APIRouter(tags=["dashboard"])
@router.get("/dashboard")
def dashboard():
    return {"scheduled":12,"unread_inbox":7,"new_leads":4,"reach_7d":18420,"engagement_rate":5.8,"autopilot":"ready"}
