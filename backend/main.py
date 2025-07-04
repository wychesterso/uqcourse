from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "courses.db"

def get_course_from_db(course_code: str):
    course_code = course_code.upper()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
            SELECT course_code, title, description, prerequisites, incompatible
            FROM courses
            WHERE course_code = ?
    """, (course_code,))
    row = cur.fetchone()

    conn.close()

    if row:
        return {
                "course_code": row[0],
                "title": row[1],
                "description": row[2],
                "prerequisites": row[3],
                "incompatible": row[4]
        }
    return None

@app.get("/api/course/{course_code}")
def get_course(course_code: str):
    course = get_course_from_db(course_code)
    if course:
        return course
    raise HTTPException(status_code=404, detail="Course not found!")
