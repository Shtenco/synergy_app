import secrets
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException
from ..security import current_context

router=APIRouter(prefix="/integrations",tags=["integrations"])
PROVIDERS={
 "vk":{"authorize":"https://id.vk.com/authorize","scopes":["vkid.personal_info"]},
 "meta":{"authorize":"https://www.facebook.com/v23.0/dialog/oauth","scopes":["pages_show_list","pages_read_engagement","pages_manage_posts","instagram_basic","instagram_content_publish","business_management"]},
}

@router.get("")
def providers(ctx=Depends(current_context)):
    return {"providers":[{"id":"vk","mode":"oauth2"},{"id":"meta","mode":"oauth2"},{"id":"telegram","mode":"bot_token"},{"id":"whatsapp","mode":"meta_embedded_signup"}],"workspace_id":ctx["workspace_id"]}

@router.post("/{provider}/authorize")
def authorize(provider:str,client_id:str,redirect_uri:str,ctx=Depends(current_context)):
    cfg=PROVIDERS.get(provider)
    if not cfg: raise HTTPException(400,"Provider uses another connection flow or is unsupported")
    state=secrets.token_urlsafe(32)
    params={"client_id":client_id,"redirect_uri":redirect_uri,"response_type":"code","state":state}
    if provider=="meta": params["scope"]=",".join(cfg["scopes"])
    return {"authorization_url":cfg["authorize"]+"?"+urlencode(params),"state":state,"store_state_server_side":True,"note":"Exchange OAuth codes only on backend and write resulting tokens to external secret vault; the database stores credentials_ref only."}
