import os
os.environ["DATABASE_URL"]="sqlite:///./test_smm.db"
os.environ["JWT_SECRET"]="test-secret"
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    assert client.get("/health").status_code==200

def test_register_brand_calendar_autopilot():
    r=client.post("/v1/auth/register",json={"email":"owner@example.com","password":"password123","workspace_name":"Demo"})
    assert r.status_code in (200,409)
    if r.status_code==409:
        r=client.post("/v1/auth/login",json={"email":"owner@example.com","password":"password123"})
    h={"Authorization":"Bearer "+r.json()["access_token"]}
    b=client.post("/v1/brands",headers=h,json={"name":"SINERGY","tone_of_voice":"confident","target_audience":"entrepreneurs"})
    assert b.status_code==200
    bid=b.json()["id"]
    assert client.post(f"/v1/brands/{bid}/knowledge",headers=h,json={"title":"Offer","content":"AI SMM OS"}).status_code==200
    assert client.post("/v1/calendar",headers=h,json={"brand_id":bid,"body":"Launch post","networks":["telegram"]}).status_code==200
    p=client.post("/v1/autopilot/plan",headers=h,json={"brand_id":bid,"horizon_days":7})
    assert p.status_code==200 and len(p.json()["content_plan"])==7
