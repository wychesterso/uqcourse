import requests

BASE_URL = "http://backend:8000"

def test_api_not_found():
    code = "ABCD0000"
    res = requests.get(f"{BASE_URL}/api/course/{code}")
    assert res.status_code == 200

    data = res.json()
    assert data["course_code"] == code
    assert data["title"] == "N/A"

def test_api_scrapes_and_returns(monkeypatch):
    res = requests.get(f"{BASE_URL}/api/course/CSSE1001")
    assert res.status_code == 200
    assert "course_code" in res.json()
