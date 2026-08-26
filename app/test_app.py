from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app

client = TestClient(app)  # type: ignore[arg-type]  # pyright resolves this dir as both "app" module and namespace package

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@patch("app.get_connection")
def test_get_items(mock_get_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {"id": 1, "name": "Keyboard", "created_at": "2026-01-01"}
    ]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Keyboard", "created_at": "2026-01-01"}
    ]

@patch("app.get_connection")
def test_add_item(mock_get_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 4
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    response = client.post("/items/TestItem")
    assert response.status_code == 200
    assert response.json()["name"] == "TestItem"
    assert response.json()["id"] == 4
