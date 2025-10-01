import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert data.get("app")
    assert data.get("version")
