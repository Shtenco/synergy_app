import json
from redis import Redis
from .config import settings

def redis_client()->Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True)

def put_json(key:str,value:dict,ttl:int): redis_client().setex(key,ttl,json.dumps(value))
def pop_json(key:str):
    r=redis_client(); raw=r.get(key)
    if raw is None: return None
    r.delete(key); return json.loads(raw)
