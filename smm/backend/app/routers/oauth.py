from __future__ import annotations
import base64,hashlib,secrets
from urllib.parse import urlencode
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..domain.models import Brand,SocialAccount
from ..security import current_context
from ..redis_client import put_json,pop_json
from ..providers import PROVIDERS
from ..vault import vault

router=APIRouter(prefix="/oauth",tags=["oauth"])

def _pkce():
    verifier=secrets.token_urlsafe(48)
    challenge=base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=')
    return verifier,challenge

@router.post("/{provider}/start")
def start(provider:str,brand_id:str,redirect_uri:str|None=None,ctx=Depends(current_context),db:Session=Depends(get_db)):
    b=db.query(Brand).filter_by(id=brand_id,workspace_id=ctx["workspace_id"]).first()
    if not b: raise HTTPException(404,"Brand not found")
    state=secrets.token_urlsafe(32); verifier,challenge=_pkce(); redirect_uri=redirect_uri or f"{settings.public_base_url}/v1/oauth/{provider}/callback"
    if provider=="vk":
        if not settings.vk_client_id: raise HTTPException(409,"VK_CLIENT_ID is not configured")
        params={"response_type":"code","client_id":settings.vk_client_id,"redirect_uri":redirect_uri,"state":state,"code_challenge":challenge,"code_challenge_method":"S256","scope":"email phone"}
        url="https://id.vk.com/authorize?"+urlencode(params)
    elif provider=="meta":
        if not settings.meta_app_id: raise HTTPException(409,"META_APP_ID is not configured")
        scopes="pages_show_list,pages_read_engagement,pages_manage_posts,instagram_basic,instagram_content_publish,business_management,whatsapp_business_management,whatsapp_business_messaging"
        params={"response_type":"code","client_id":settings.meta_app_id,"redirect_uri":redirect_uri,"state":state,"scope":scopes}
        url=f"https://www.facebook.com/{settings.meta_graph_version}/dialog/oauth?"+urlencode(params)
    else: raise HTTPException(400,"This provider does not use authorization-code OAuth")
    put_json(f"sinergy:smm:oauth:{state}",{"workspace_id":ctx["workspace_id"],"brand_id":brand_id,"provider":provider,"redirect_uri":redirect_uri,"code_verifier":verifier},600)
    return {"authorization_url":url,"state":state,"expires_in":600}

@router.get("/{provider}/callback")
async def callback(provider:str,code:str,state:str,device_id:str="",db:Session=Depends(get_db)):
    flow=pop_json(f"sinergy:smm:oauth:{state}")
    if not flow or flow.get("provider")!=provider: raise HTTPException(400,"OAuth state invalid or expired")
    adapter=PROVIDERS.get(provider)
    if not adapter: raise HTTPException(400,"Unsupported provider")
    token=await adapter.exchange_code(code,flow["redirect_uri"],flow.get("code_verifier","") ,device_id)
    ref=vault.put(f"oauth/{flow['workspace_id']}/{flow['brand_id']}/{provider}/{secrets.token_hex(8)}",{"access_token":token.access_token,"refresh_token":token.refresh_token,"expires_in":token.expires_in,"raw":token.raw or {}})
    account=SocialAccount(brand_id=flow["brand_id"],network=provider,external_id=token.external_id or f"pending:{secrets.token_hex(4)}",display_name=token.display_name or provider,status="connected",credentials_ref=ref)
    db.add(account); db.commit(); db.refresh(account)
    return {"connected":True,"social_account_id":account.id,"network":provider}
