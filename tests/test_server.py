import pytest
from fastapi.testclient import TestClient
from mcp_server.server import app

client = TestClient(app)

def test_parse_file_invalid_url():
    resp = client.post("/parse_file", json={"url": "http://invalid-url/test.xlsx"})
    assert resp.status_code == 200
    assert "error" in resp.json() 