from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routers import health, auth, brands, calendar, inbox, analytics, autopilot, integrations, dashboard, content, leads, oauth, ai_studio, publishing, webhooks

Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.app_name,version="1.2.0")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(",")],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(health.router)
for router in [auth.router,brands.router,calendar.router,inbox.router,analytics.router,autopilot.router,integrations.router,dashboard.router,content.router,leads.router,oauth.router,ai_studio.router,publishing.router,webhooks.router]:
    app.include_router(router,prefix="/v1")
