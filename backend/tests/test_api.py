import os
import sys
from pathlib import Path
import importlib.util

os.environ.setdefault("OPENAI_API_KEY", "test")

root = Path(__file__).resolve().parents[1]
sys.path.append(str(root))

spec = importlib.util.spec_from_file_location("backend_main", root / "main.py")
backend_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_main)
app = backend_main.app

from fastapi.testclient import TestClient
client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["message"].startswith("AI ServiceNow")

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"
