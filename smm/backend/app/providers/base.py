from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass
class OAuthTokenSet:
    access_token:str
    refresh_token:str=""
    expires_in:int=0
    external_id:str=""
    display_name:str=""
    raw:dict|None=None

class SocialProvider(Protocol):
    name:str
    async def exchange_code(self, code:str, redirect_uri:str, code_verifier:str="", device_id:str="")->OAuthTokenSet: ...
    async def publish(self, credentials:dict, payload:dict)->dict: ...
    async def normalize_webhook(self, payload:dict, headers:dict)->list[dict]: ...
