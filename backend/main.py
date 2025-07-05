from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

from scraper import scrape_course_details

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "courses.db"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_conn():
    return sqlite3.connect(DB_PATH)

def setup_db():
    with get_db_conn() as conn:
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

@app.on_event("startup")
def on_startup():
    setup_db()

def get_course_from_db(course_code: str):
    course_code = course_code.upper()

    with get_db_conn() as conn:
        cur = conn.cursor()

        cur.execute("""
            SELECT course_code, title, faculty, semesters, prerequisites, incompatible, description
            FROM courses
            WHERE course_code = ?
        """, (course_code,))
        row = cur.fetchone()

        if row:
            return {
                "course_code": row[0],
                "title": row[1],
                "faculty": row[2],
                "semesters": row[3],
                "prerequisites": row[4],
                "incompatible": row[5],
                "description": row[6]
            }
        return None

def insert_course(course):
    with get_db_conn() as conn:
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
        """, course)
        conn.commit()

@app.get("/api/course/{course_code}")
def get_course(course_code: str):
    course_code = course_code.upper()
    course = get_course_from_db(course_code)

    if course:
        return course

    scraped = scrape_course_details(course_code)
    if scraped:
        insert_course(scraped)
        return scraped

    raise HTTPException(status_code=404, detail="Course not found!")
