import httpx
from ..config import settings
class WhatsAppProvider:
    name="whatsapp"
    async def exchange_code(self,*a,**k): raise RuntimeError("WhatsApp account connection uses Meta business flow")
    async def publish(self,credentials,payload):
        phone_id=credentials["phone_number_id"]
        async with httpx.AsyncClient(timeout=20) as c:
            r=await c.post(f"https://graph.facebook.com/{settings.meta_graph_version}/{phone_id}/messages",headers={"Authorization":f"Bearer {credentials['access_token']}"},json={"messaging_product":"whatsapp","to":payload["to"],"type":"text","text":{"body":payload.get("body","")}}); r.raise_for_status(); return r.json()
    async def normalize_webhook(self,payload,headers):
        events=[]
        for entry in payload.get("entry",[]):
            for change in entry.get("changes",[]):
                val=change.get("value",{})
                for m in val.get("messages",[]):
                    text=(m.get("text") or {}).get("body","")
                    events.append({"kind":"message","external_thread_id":m.get("from",""),"external_message_id":m.get("id",""),"contact_id":m.get("from",""),"body":text})
        return events
