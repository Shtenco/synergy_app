from __future__ import annotations
import re
import httpx
from sqlalchemy.orm import Session
from .config import settings
from .domain.models import Brand, BrandKnowledge

def _tokens(s:str)->set[str]: return set(re.findall(r"[a-zа-я0-9]{3,}",s.lower()))
def retrieve_brand_context(db:Session,brand_id:str,query:str,limit:int=6)->list[BrandKnowledge]:
    q=_tokens(query); rows=db.query(BrandKnowledge).filter_by(brand_id=brand_id).all()
    return sorted(rows,key=lambda x:len(q&_tokens(f"{x.title} {x.content} {' '.join(x.tags or [])}")),reverse=True)[:limit]

async def generate(db:Session,brand:Brand,prompt:str,purpose:str="content")->dict:
    docs=retrieve_brand_context(db,brand.id,prompt)
    context="\n\n".join(f"[{d.kind}] {d.title}: {d.content}" for d in docs)
    system=f"You are SINERGY SMM AI. Brand: {brand.name}. Tone: {brand.tone_of_voice}. Audience: {brand.target_audience}. Use only factual claims supported by Brand Brain. Purpose: {purpose}."
    if settings.ai_base_url and settings.ai_api_key and settings.ai_model:
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as c:
            r=await c.post(settings.ai_base_url.rstrip('/')+"/chat/completions",headers={"Authorization":f"Bearer {settings.ai_api_key}"},json={"model":settings.ai_model,"messages":[{"role":"system","content":system},{"role":"user","content":f"BRAND BRAIN:\n{context}\n\n{prompt}"}],"temperature":0.6}); r.raise_for_status(); data=r.json()
        text=data["choices"][0]["message"]["content"]
    else:
        key=(docs[0].content[:350] if docs else brand.description[:350])
        text=f"{prompt.strip()}\n\n{key}".strip()
    return {"text":text,"sources":[{"id":d.id,"title":d.title,"kind":d.kind} for d in docs],"model":settings.ai_model or "local-fallback"}
