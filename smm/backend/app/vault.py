from __future__ import annotations
import json
from dataclasses import dataclass
import httpx
from .config import settings

class VaultError(RuntimeError): pass

@dataclass
class SecretVault:
    """Secret-vault facade. Production uses HashiCorp Vault KV v2; memory is dev-only."""
    _memory: dict[str, dict] = None
    def __post_init__(self):
        if self._memory is None: self._memory={}
    def put(self, path:str, value:dict)->str:
        if settings.vault_addr and settings.vault_token:
            url=f"{settings.vault_addr.rstrip('/')}/v1/{settings.vault_mount}/data/{path.lstrip('/')}"
            r=httpx.post(url,headers={"X-Vault-Token":settings.vault_token},json={"data":value},timeout=15)
            if r.status_code>=300: raise VaultError(f"vault put failed: {r.status_code}")
            return f"vault://{settings.vault_mount}/{path}"
        if settings.env not in {"dev","test"}: raise VaultError("Production requires VAULT_ADDR and VAULT_TOKEN")
        self._memory[path]=json.loads(json.dumps(value))
        return f"memory://{path}"
    def get(self, ref:str)->dict:
        if ref.startswith("vault://"):
            _,rest=ref.split("vault://",1); mount,path=rest.split("/",1)
            url=f"{settings.vault_addr.rstrip('/')}/v1/{mount}/data/{path}"
            r=httpx.get(url,headers={"X-Vault-Token":settings.vault_token},timeout=15)
            if r.status_code>=300: raise VaultError(f"vault get failed: {r.status_code}")
            return r.json()["data"]["data"]
        if ref.startswith("memory://"): return self._memory.get(ref.removeprefix("memory://"),{})
        raise VaultError("Unknown vault reference")

vault=SecretVault()
