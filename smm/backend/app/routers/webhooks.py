from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter,Request,HTTPException,Query
from ..database import SessionLocal
from ..domain.models import SocialAccount,Conversation,Message,Brand,Lead
from ..providers import PROVIDERS
from ..config import settings
from ..ai import generate
router=APIRouter(prefix="/webhooks",tags=["webhooks"])

@router.get("/meta")
def meta_verify(hub_mode:str=Query("",alias="hub.mode"),hub_verify_token:str=Query("",alias="hub.verify_token"),hub_challenge:str=Query("",alias="hub.challenge")):
    if hub_mode=="subscribe" and hub_verify_token==settings.meta_webhook_verify_token: return int(hub_challenge) if hub_challenge.isdigit() else hub_challenge
    raise HTTPException(403,"Verification failed")

@router.post("/{network}/{account_id}")
async def ingest(network:str,account_id:str,request:Request):
    db=SessionLocal()
    try:
        account=db.get(SocialAccount,account_id)
        if not account or account.network not in {network,"meta"}: raise HTTPException(404,"Account not found")
        if network=="telegram" and settings.telegram_webhook_secret:
            if request.headers.get("X-Telegram-Bot-Api-Secret-Token")!=settings.telegram_webhook_secret: raise HTTPException(403,"Bad webhook secret")
        adapter=PROVIDERS.get(network)
        if not adapter: raise HTTPException(400,"Unsupported network")
        payload=await request.json(); events=await adapter.normalize_webhook(payload,dict(request.headers))
        created=0
        for ev in events:
            thread=ev.get("external_thread_id","")
            conv=db.query(Conversation).filter_by(brand_id=account.brand_id,network=network,external_thread_id=thread).first()
            if not conv:
                conv=Conversation(brand_id=account.brand_id,network=network,external_thread_id=thread,contact_name=ev.get("contact_name","") or ev.get("contact_id",""),unread_count=0); db.add(conv); db.flush()
            ext=ev.get("external_message_id","")
            if ext and db.query(Message).filter_by(conversation_id=conv.id,external_message_id=ext).first(): continue
            brand=db.get(Brand,account.brand_id)
            draft=await generate(db,brand,f"Draft a helpful reply to this inbound customer message: {ev.get('body','')}","reply")
            msg=Message(conversation_id=conv.id,external_message_id=ext,direction="inbound",body=ev.get("body",""),ai_suggested=True,ai_draft=draft["text"])
            conv.unread_count+=1; conv.last_message_at=datetime.utcnow(); db.add(msg); created+=1
            lead=db.query(Lead).filter_by(workspace_id=brand.workspace_id,brand_id=brand.id,source=network,source_detail=thread).first()
            if not lead: db.add(Lead(workspace_id=brand.workspace_id,brand_id=brand.id,name=conv.contact_name,source=network,source_detail=thread,score=50,attribution={"conversation_id":conv.id,"network":network}))
        db.commit(); return {"ok":True,"ingested":created}
    finally: db.close()
