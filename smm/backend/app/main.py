from fastapi import FastAPI
from .routers import health, dashboard, content, leads

app = FastAPI(title="SINERGY SMM API", version="1.0.0")
app.include_router(health.router)
app.include_router(dashboard.router, prefix="/v1")
app.include_router(content.router, prefix="/v1")
app.include_router(leads.router, prefix="/v1")
