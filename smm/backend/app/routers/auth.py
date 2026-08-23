from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..domain.models import User, Workspace, Membership
from ..schemas import RegisterIn, LoginIn, TokenOut
from ..security import hash_password, verify_password, create_token
router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register", response_model=TokenOut)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email.lower()).first(): raise HTTPException(409, "Email already registered")
    u=User(email=data.email.lower(),password_hash=hash_password(data.password),display_name=data.display_name); db.add(u); db.flush()
    w=Workspace(name=data.workspace_name,owner_id=u.id); db.add(w); db.flush(); db.add(Membership(workspace_id=w.id,user_id=u.id,role="owner")); db.commit()
    return TokenOut(access_token=create_token(u.id,w.id),workspace_id=w.id)
@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    u=db.query(User).filter(User.email == data.email.lower()).first()
    if not u or not verify_password(data.password,u.password_hash): raise HTTPException(401,"Invalid credentials")
    m=db.query(Membership).filter_by(user_id=u.id).first()
    if not m: raise HTTPException(403,"No workspace")
    return TokenOut(access_token=create_token(u.id,m.workspace_id),workspace_id=m.workspace_id)
