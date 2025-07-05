import pytest
from scraper import scrape_course_details
import requests

def sample_course_html():
    return """
    <html>
        <h1 id="course-title">Intro to Something (ABCD1001)</h1>
        <p id="course-faculty">Faculty of Something</p>
        <p id="course-summary">This course teaches nothing!</p>
        <p id="course-prerequisite">ABCD1000</p>
        <p id="course-incompatible">EFGH1001</p>
        <table id="course-current-offerings">
            <td><a class="course-offering-year">Semester 1, 2025</a></td>
            <td><a class="course-offering-year">Semester 2, 2025</a></td>
        </table>
    </html>
    """

def test_scrape_valid_course(monkeypatch):
    class MockResponse:
        ok = True
        text = sample_course_html()

    monkeypatch.setattr(requests, "get", lambda url: MockResponse())
    data = scrape_course_details("abcd1000")

    assert data["course_code"] == "ABCD1000"
    assert data["title"] == "Intro to Something"
    assert data["faculty"] == "Faculty of Something"
    assert data["description"] == "This course teaches nothing!"
    assert "Semester 1" in data["semesters"]
