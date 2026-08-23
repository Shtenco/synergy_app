from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from .domain.models import User, Membership

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)

def hash_password(v: str) -> str: return pwd.hash(v)
def verify_password(v: str, h: str) -> bool: return pwd.verify(v, h)
def create_token(user_id: str, workspace_id: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    return jwt.encode({"sub": user_id, "wid": workspace_id, "exp": exp}, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def current_context(creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    if not creds: raise HTTPException(401, "Authentication required")
    try: payload = jwt.decode(creds.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError: raise HTTPException(401, "Invalid token")
    user = db.get(User, payload.get("sub")); wid = payload.get("wid")
    if not user or not wid: raise HTTPException(401, "Invalid token")
    membership = db.query(Membership).filter_by(user_id=user.id, workspace_id=wid).first()
    if not membership: raise HTTPException(403, "Workspace access denied")
    return {"user": user, "workspace_id": wid, "role": membership.role}
