from __future__ import annotations
import json,time,uuid
from .redis_client import redis_client
from .config import settings
QUEUE="sinergy:smm:publish"
DELAYED="sinergy:smm:publish:delayed"
DLQ="sinergy:smm:publish:dead"

def enqueue(payload:dict, idempotency_key:str)->dict:
    r=redis_client(); guard=f"sinergy:smm:idem:{idempotency_key}"
    if not r.set(guard,"1",nx=True,ex=7*24*3600): return {"queued":False,"duplicate":True}
    job={"job_id":str(uuid.uuid4()),"idempotency_key":idempotency_key,"attempt":0,"payload":payload}
    r.rpush(QUEUE,json.dumps(job)); return {"queued":True,"job_id":job["job_id"]}

def reserve(timeout:int=5):
    r=redis_client(); item=r.blpop(QUEUE,timeout=timeout)
    return json.loads(item[1]) if item else None

def retry(job:dict,error:str):
    r=redis_client(); job["attempt"]=int(job.get("attempt",0))+1; job["error"]=error[:2000]
    if job["attempt"]>=settings.publish_max_attempts: r.rpush(DLQ,json.dumps(job)); return "dead"
    delay=min(300,2**job["attempt"]*5); r.zadd(DELAYED,{json.dumps(job):time.time()+delay}); return "retry"

def pump_delayed():
    r=redis_client(); now=time.time(); rows=r.zrangebyscore(DELAYED,0,now)
    if rows:
        pipe=r.pipeline()
        for row in rows: pipe.rpush(QUEUE,row); pipe.zrem(DELAYED,row)
        pipe.execute()
    return len(rows)
