from fastapi import APIRouter
router=APIRouter(prefix="/leads", tags=["leads"])
@router.get("")
def leads(): return [{"id":"lead_001","source":"vk","stage":"new","score":87,"name":"Demo Lead"}]
