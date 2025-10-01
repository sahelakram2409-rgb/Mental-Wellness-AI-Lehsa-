import sys
from pathlib import Path

# Add project root to Python path BEFORE any app imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Also add current working directory as fallback
import os
current_dir = os.getcwd()
if str(project_root) != current_dir:
    sys.path.insert(0, current_dir)

# Now import the app and test client
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert data.get("app")
    assert data.get("version")
