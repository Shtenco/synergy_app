import asyncio
from datetime import datetime
from backend.app.database import SessionLocal
from backend.app.domain.models import PublicationDelivery,ContentItem,SocialAccount
from backend.app.queue import reserve,retry,pump_delayed
from backend.app.providers import PROVIDERS
from backend.app.vault import vault

async def handle(job:dict):
    db=SessionLocal()
    try:
        delivery=db.get(PublicationDelivery,job["payload"]["delivery_id"])
        if not delivery or delivery.status=="published": return
        item=db.get(ContentItem,delivery.content_id); account=db.get(SocialAccount,delivery.social_account_id)
        if not item or not account: raise RuntimeError("delivery references missing content/account")
        adapter=PROVIDERS.get(account.network)
        if not adapter: raise RuntimeError(f"provider not supported: {account.network}")
        credentials=vault.get(account.credentials_ref)
        delivery.status="publishing"; delivery.attempts+=1; delivery.updated_at=datetime.utcnow(); db.commit()
        result=await adapter.publish(credentials,{"body":item.body,"external_id":account.external_id,**(account.metadata_json or {})})
        delivery.status="published"; delivery.external_post_id=str(result.get("id") or result.get("post_id") or result.get("result",{}).get("post_id",'')); delivery.last_error=""; delivery.updated_at=datetime.utcnow(); item.status="published"; item.published_at=datetime.utcnow(); db.commit()
    except Exception as e:
        try:
            if 'delivery' in locals() and delivery:
                delivery.status="retrying"; delivery.last_error=str(e)[:2000]; delivery.updated_at=datetime.utcnow(); db.commit()
        finally: retry(job,str(e))
    finally: db.close()

async def publication_loop():
    while True:
        try:
            pump_delayed(); job=reserve(timeout=2)
            if job: await handle(job)
        except Exception:
            await asyncio.sleep(2)

if __name__ == "__main__": asyncio.run(publication_loop())
