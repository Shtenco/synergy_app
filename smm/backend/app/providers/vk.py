import httpx
from .base import OAuthTokenSet
from ..config import settings
class VKProvider:
    name="vk"
    async def exchange_code(self,code,redirect_uri,code_verifier="",device_id=""):
        data={"grant_type":"authorization_code","code":code,"client_id":settings.vk_client_id,"redirect_uri":redirect_uri,"code_verifier":code_verifier,"device_id":device_id}
        async with httpx.AsyncClient(timeout=20) as c:
            r=await c.post("https://id.vk.com/oauth2/auth",data=data); r.raise_for_status(); t=r.json()
        return OAuthTokenSet(t.get("access_token",""),t.get("refresh_token",""),int(t.get("expires_in",0)),raw=t)
    async def publish(self,credentials,payload):
        params={"access_token":credentials["access_token"],"v":settings.vk_api_version,"message":payload.get("body","")}
        if payload.get("owner_id"): params["owner_id"]=payload["owner_id"]
        async with httpx.AsyncClient(timeout=20) as c:
            r=await c.post("https://api.vk.com/method/wall.post",data=params); r.raise_for_status(); return r.json()
    async def normalize_webhook(self,payload,headers):
        if payload.get("type")!="message_new": return []
        obj=payload.get("object",{}).get("message",{})
        return [{"kind":"message","external_thread_id":str(obj.get("peer_id","")),"external_message_id":str(obj.get("id","")),"contact_id":str(obj.get("from_id","")),"body":obj.get("text","")}]
