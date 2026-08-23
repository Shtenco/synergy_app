import httpx
from .base import OAuthTokenSet
from ..config import settings
class MetaProvider:
    name="meta"
    async def exchange_code(self,code,redirect_uri,code_verifier="",device_id=""):
        params={"client_id":settings.meta_app_id,"client_secret":settings.meta_app_secret,"redirect_uri":redirect_uri,"code":code}
        async with httpx.AsyncClient(timeout=20) as c:
            r=await c.get(f"https://graph.facebook.com/{settings.meta_graph_version}/oauth/access_token",params=params); r.raise_for_status(); t=r.json()
        return OAuthTokenSet(t.get("access_token",""),expires_in=int(t.get("expires_in",0)),raw=t)
    async def publish(self,credentials,payload):
        account=payload.get("external_id") or credentials.get("external_id")
        async with httpx.AsyncClient(timeout=30) as c:
            r=await c.post(f"https://graph.facebook.com/{settings.meta_graph_version}/{account}/feed",data={"message":payload.get("body",""),"access_token":credentials["access_token"]}); r.raise_for_status(); return r.json()
    async def normalize_webhook(self,payload,headers):
        events=[]
        for entry in payload.get("entry",[]):
            for msg in entry.get("messaging",[]):
                body=(msg.get("message") or {}).get("text","")
                if body: events.append({"kind":"message","external_thread_id":str((msg.get("sender") or {}).get("id","")),"external_message_id":str((msg.get("message") or {}).get("mid","")),"contact_id":str((msg.get("sender") or {}).get("id","")),"body":body})
        return events
