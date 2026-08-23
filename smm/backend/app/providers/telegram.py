import httpx
class TelegramProvider:
    name="telegram"
    async def exchange_code(self,*a,**k): raise RuntimeError("Telegram uses bot token, not OAuth code")
    async def publish(self,credentials,payload):
        token=credentials["bot_token"]; chat_id=payload.get("external_id") or credentials.get("chat_id")
        async with httpx.AsyncClient(timeout=20) as c:
            r=await c.post(f"https://api.telegram.org/bot{token}/sendMessage",json={"chat_id":chat_id,"text":payload.get("body","")}); r.raise_for_status(); return r.json()
    async def normalize_webhook(self,payload,headers):
        m=payload.get("message") or payload.get("channel_post") or {}
        if not m: return []
        chat=m.get("chat") or {}; sender=m.get("from") or {}
        return [{"kind":"message","external_thread_id":str(chat.get("id","")),"external_message_id":str(m.get("message_id","")),"contact_id":str(sender.get("id",chat.get("id",""))),"contact_name":" ".join(x for x in [sender.get("first_name",""),sender.get("last_name","")] if x),"body":m.get("text") or m.get("caption") or ""}]
