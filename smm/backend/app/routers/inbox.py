from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand, Conversation, Message
from ..security import current_context
router=APIRouter(prefix="/inbox",tags=["inbox"])
@router.get("")
def inbox(ctx=Depends(current_context),db:Session=Depends(get_db)):
    ids=[b.id for b in db.query(Brand).filter_by(workspace_id=ctx["workspace_id"]).all()]
    return db.query(Conversation).filter(Conversation.brand_id.in_(ids)).order_by(Conversation.last_message_at.desc()).all() if ids else []
@router.get("/{conversation_id}/messages")
def messages(conversation_id:str,ctx=Depends(current_context),db:Session=Depends(get_db)):
    conv=db.get(Conversation,conversation_id); brand=db.get(Brand,conv.brand_id) if conv else None
    if not conv or not brand or brand.workspace_id!=ctx["workspace_id"]: raise HTTPException(404,"Conversation not found")
    return db.query(Message).filter_by(conversation_id=conv.id).order_by(Message.sent_at).all()
@router.post("/{conversation_id}/read")
def read(conversation_id:str,ctx=Depends(current_context),db:Session=Depends(get_db)):
    conv=db.get(Conversation,conversation_id); brand=db.get(Brand,conv.brand_id) if conv else None
    if not conv or not brand or brand.workspace_id!=ctx["workspace_id"]: raise HTTPException(404,"Conversation not found")
    conv.unread_count=0; db.commit(); return {"ok":True}
