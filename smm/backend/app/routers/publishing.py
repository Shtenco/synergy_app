from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import Brand,ContentItem,SocialAccount,PublicationDelivery
from ..security import current_context
from ..queue import enqueue
router=APIRouter(prefix="/publishing",tags=["publishing"])
@router.post("/{content_id}/enqueue")
def publish(content_id:str,ctx=Depends(current_context),db:Session=Depends(get_db)):
    item=db.get(ContentItem,content_id)
    brand=db.get(Brand,item.brand_id) if item else None
    if not item or not brand or brand.workspace_id!=ctx["workspace_id"]: raise HTTPException(404,"Content not found")
    accounts=db.query(SocialAccount).filter(SocialAccount.brand_id==brand.id,SocialAccount.network.in_(item.networks),SocialAccount.status=="connected").all()
    if not accounts: raise HTTPException(409,"No connected account for selected networks")
    results=[]
    for acc in accounts:
        idem=f"{content_id}:{acc.id}:{item.scheduled_at.isoformat() if item.scheduled_at else 'now'}"
        delivery=db.query(PublicationDelivery).filter_by(idempotency_key=idem).first()
        if not delivery:
            delivery=PublicationDelivery(content_id=item.id,social_account_id=acc.id,idempotency_key=idem); db.add(delivery); db.commit(); db.refresh(delivery)
        q=enqueue({"delivery_id":delivery.id},idem); results.append({"delivery_id":delivery.id,"network":acc.network,**q})
    return {"deliveries":results}
