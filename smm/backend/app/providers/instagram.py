import httpx
from ..config import settings
class InstagramProvider:
    name="instagram"
    async def exchange_code(self,*args,**kwargs):
        from .meta import MetaProvider
        return await MetaProvider().exchange_code(*args,**kwargs)
    async def publish(self,credentials,payload):
        ig_user_id=payload.get("external_id") or credentials.get("external_id")
        image_url=payload.get("image_url"); video_url=payload.get("video_url")
        if not (image_url or video_url): raise RuntimeError("Instagram publishing requires image_url or video_url")
        create={"caption":payload.get("body",""),"access_token":credentials["access_token"]}
        if image_url: create["image_url"]=image_url
        if video_url: create.update({"video_url":video_url,"media_type":"REELS"})
        async with httpx.AsyncClient(timeout=60) as c:
            r=await c.post(f"https://graph.facebook.com/{settings.meta_graph_version}/{ig_user_id}/media",data=create); r.raise_for_status(); creation=r.json()["id"]
            r=await c.post(f"https://graph.facebook.com/{settings.meta_graph_version}/{ig_user_id}/media_publish",data={"creation_id":creation,"access_token":credentials["access_token"]}); r.raise_for_status(); return r.json()
    async def normalize_webhook(self,payload,headers):
        events=[]
        for entry in payload.get("entry",[]):
            for msg in entry.get("messaging",[]):
                body=(msg.get("message") or {}).get("text","")
                if body: events.append({"kind":"message","external_thread_id":str((msg.get("sender") or {}).get("id","")),"external_message_id":str((msg.get("message") or {}).get("mid","")),"contact_id":str((msg.get("sender") or {}).get("id","")),"body":body})
        return events
