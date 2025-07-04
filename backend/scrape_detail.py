import sqlite3
import requests
from bs4 import BeautifulSoup

DB_PATH = "courses.db"

def setup_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_code TEXT PRIMARY KEY,
                title TEXT,
                faculty TEXT,
                semesters TEXT,
                prerequisites TEXT,
                incompatible TEXT,
                description TEXT
            )
        """)
        conn.commit()

def scrape_course_details(course_code: str):
    url = f"https://programs-courses.uq.edu.au/course.html?course_code={course_code.lower()}"
    resp = requests.get(url)
    if not resp.ok:
        print(f"Failed to fetch {course_code}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    title_block = soup.find("h1", id="course-title")
    title = title_block.text.split(" (")[0].strip() if title_block else "N/A"

    faculty = soup.find("p", id="course-faculty")
    faculty_text = faculty.text.strip() if faculty else "N/A"

    prereq = soup.find("p", id="course-prerequisite")
    prereq_text = prereq.text.strip() if prereq else ""

    incompatible = soup.find("p", id="course-incompatible")
    incompatible_text = incompatible.text.strip() if incompatible else ""

    description = soup.find("p", id="course-summary")
    description_text = description.text.strip() if description else ""

    # Look for 2025 semester offerings
    semesters = []
    offerings = soup.select("table#course-current-offerings td a.course-offering-year")
    for offer in offerings:
        text = offer.get_text(strip=True)
        if "2025" in text:
            if "Semester 1" in text:
                semesters.append("Semester 1")
            elif "Semester 2" in text:
                semesters.append("Semester 2")
            elif "Summer Semester" in text:
                semesters.append("Summer Semester")

    semesters = ", ".join(sorted(set(semesters)))

    return {
        "course_code": course_code.upper(),
        "title": title,
        "faculty": faculty_text,
        "semesters": semesters,
        "prerequisites": prereq_text,
        "incompatible": incompatible_text,
        "description": description_text,
    }

def update_course(course_data):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO courses (course_code, title, faculty, semesters, prerequisites, incompatible, description)
            VALUES (:course_code, :title, :faculty, :semesters, :prerequisites, :incompatible, :description)
            ON CONFLICT(course_code) DO UPDATE SET
                title = excluded.title,
                faculty = excluded.faculty,
                semesters = excluded.semesters,
                prerequisites = excluded.prerequisites,
                incompatible = excluded.incompatible,
                description = excluded.description
        """, course_data)
        conn.commit()

def main():
    setup_db()
    with open("course_codes.txt") as f:
        codes = [line.strip() for line in f if line.strip()]

    for code in codes:
        print(f"Scraping {code}...")
        data = scrape_course_details(code)
        if data:
            update_course(data)

if __name__ == "__main__":
    main()
