import enum
import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Boolean, JSON, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

def uid(): return str(uuid.uuid4())

class ContentStatus(str, enum.Enum):
    draft="draft"; review="review"; scheduled="scheduled"; published="published"; failed="failed"
class LeadStage(str, enum.Enum):
    new="new"; qualified="qualified"; offer="offer"; won="won"; lost="lost"

class User(Base):
    __tablename__="users"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid)
    email: Mapped[str]=mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    display_name: Mapped[str]=mapped_column(String(120), default="")
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Workspace(Base):
    __tablename__="workspaces"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid)
    name: Mapped[str]=mapped_column(String(160))
    owner_id: Mapped[str]=mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Membership(Base):
    __tablename__="memberships"; __table_args__=(UniqueConstraint("workspace_id","user_id"),)
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid)
    workspace_id: Mapped[str]=mapped_column(ForeignKey("workspaces.id"), index=True)
    user_id: Mapped[str]=mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[str]=mapped_column(String(32), default="owner")

class Brand(Base):
    __tablename__="brands"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid)
    workspace_id: Mapped[str]=mapped_column(ForeignKey("workspaces.id"), index=True)
    name: Mapped[str]=mapped_column(String(160)); description: Mapped[str]=mapped_column(Text, default="")
    tone_of_voice: Mapped[str]=mapped_column(Text, default=""); target_audience: Mapped[str]=mapped_column(Text, default="")
    goals: Mapped[dict]=mapped_column(JSON, default=dict)

class SocialAccount(Base):
    __tablename__="social_accounts"; __table_args__=(UniqueConstraint("brand_id","network","external_id"),)
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid)
    brand_id: Mapped[str]=mapped_column(ForeignKey("brands.id"), index=True)
    network: Mapped[str]=mapped_column(String(32), index=True); external_id: Mapped[str]=mapped_column(String(255))
    display_name: Mapped[str]=mapped_column(String(255), default=""); status: Mapped[str]=mapped_column(String(32), default="connected")
    credentials_ref: Mapped[str]=mapped_column(String(255), default=""); metadata_json: Mapped[dict]=mapped_column(JSON, default=dict)

class BrandKnowledge(Base):
    __tablename__="brand_knowledge"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid)
    brand_id: Mapped[str]=mapped_column(ForeignKey("brands.id"), index=True)
    kind: Mapped[str]=mapped_column(String(40), default="note"); title: Mapped[str]=mapped_column(String(255)); content: Mapped[str]=mapped_column(Text)
    tags: Mapped[list]=mapped_column(JSON, default=list); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class ContentItem(Base):
    __tablename__="content_items"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid); brand_id: Mapped[str]=mapped_column(ForeignKey("brands.id"), index=True)
    title: Mapped[str]=mapped_column(String(255), default=""); body: Mapped[str]=mapped_column(Text)
    status: Mapped[ContentStatus]=mapped_column(Enum(ContentStatus), default=ContentStatus.draft, index=True); networks: Mapped[list]=mapped_column(JSON, default=list)
    scheduled_at: Mapped[datetime|None]=mapped_column(DateTime, nullable=True, index=True); published_at: Mapped[datetime|None]=mapped_column(DateTime, nullable=True)
    campaign_id: Mapped[str|None]=mapped_column(String(36), nullable=True, index=True); ai_generated: Mapped[bool]=mapped_column(Boolean, default=False)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__="conversations"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid); brand_id: Mapped[str]=mapped_column(ForeignKey("brands.id"), index=True)
    network: Mapped[str]=mapped_column(String(32), index=True); external_thread_id: Mapped[str]=mapped_column(String(255), index=True)
    contact_name: Mapped[str]=mapped_column(String(255), default=""); unread_count: Mapped[int]=mapped_column(Integer, default=0)
    last_message_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, index=True)

class Message(Base):
    __tablename__="messages"; __table_args__=(UniqueConstraint("conversation_id","external_message_id"),)
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid); conversation_id: Mapped[str]=mapped_column(ForeignKey("conversations.id"), index=True)
    external_message_id: Mapped[str]=mapped_column(String(255), default=""); direction: Mapped[str]=mapped_column(String(16)); body: Mapped[str]=mapped_column(Text)
    sent_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow); ai_suggested: Mapped[bool]=mapped_column(Boolean, default=False)
    ai_draft: Mapped[str]=mapped_column(Text, default="")

class PublicationDelivery(Base):
    __tablename__="publication_deliveries"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid); content_id: Mapped[str]=mapped_column(ForeignKey("content_items.id"), index=True)
    social_account_id: Mapped[str]=mapped_column(ForeignKey("social_accounts.id"), index=True); idempotency_key: Mapped[str]=mapped_column(String(180), unique=True, index=True)
    status: Mapped[str]=mapped_column(String(32), default="queued", index=True); attempts: Mapped[int]=mapped_column(Integer, default=0)
    external_post_id: Mapped[str]=mapped_column(String(255), default=""); last_error: Mapped[str]=mapped_column(Text, default="")
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow); updated_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Lead(Base):
    __tablename__="leads"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid); workspace_id: Mapped[str]=mapped_column(ForeignKey("workspaces.id"), index=True)
    brand_id: Mapped[str|None]=mapped_column(ForeignKey("brands.id"), nullable=True, index=True); name: Mapped[str]=mapped_column(String(255), default="")
    source: Mapped[str]=mapped_column(String(80), index=True); source_detail: Mapped[str]=mapped_column(String(255), default="")
    stage: Mapped[LeadStage]=mapped_column(Enum(LeadStage), default=LeadStage.new, index=True); score: Mapped[int]=mapped_column(Integer, default=0)
    value_minor: Mapped[int]=mapped_column(Integer, default=0); currency: Mapped[str]=mapped_column(String(8), default="RUB")
    attribution: Mapped[dict]=mapped_column(JSON, default=dict); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class AnalyticsEvent(Base):
    __tablename__="analytics_events"
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=uid); workspace_id: Mapped[str]=mapped_column(ForeignKey("workspaces.id"), index=True)
    brand_id: Mapped[str|None]=mapped_column(ForeignKey("brands.id"), nullable=True, index=True); event_type: Mapped[str]=mapped_column(String(80), index=True)
    network: Mapped[str]=mapped_column(String(32), default=""); entity_id: Mapped[str]=mapped_column(String(80), default="")
    value: Mapped[int]=mapped_column(Integer, default=1); payload: Mapped[dict]=mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow, index=True)
