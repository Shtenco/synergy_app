from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand, Conversation
from ..security import current_context
router=APIRouter(prefix="/inbox",tags=["inbox"])
@router.get("")
def inbox(ctx=Depends(current_context),db:Session=Depends(get_db)):
    ids=[b.id for b in db.query(Brand).filter_by(workspace_id=ctx["workspace_id"]).all()]
    return db.query(Conversation).filter(Conversation.brand_id.in_(ids)).order_by(Conversation.last_message_at.desc()).all() if ids else []
