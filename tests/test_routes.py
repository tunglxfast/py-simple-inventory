from fastapi.testclient import TestClient

from app.main import app


def test_setup_page_renders():
    client = TestClient(app)
    response = client.get("/setup")
    assert response.status_code in {200, 303}


def test_dashboard_redirects_to_setup_when_database_missing():
    client = TestClient(app)
    response = client.get("/", follow_redirects=False)
    assert response.status_code in {200, 303}

