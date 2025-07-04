import sqlite3

conn = sqlite3.connect("courses.db")
cur = conn.cursor()

cur.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_code TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            prerequisites TEXT DEFAULT '',
            incompatible TEXT DEFAULT ''
        )
""")

# dummy data
courses = [
        ("COMP1000",
         "Worst Course Ever",
         "Teaches nothing!",
         None,
         None),
        ("COMP6000",
         "Hardest Course Ever",
         "Teaches everything!",
         "COMP1000",
         "COMP6001"),
]

cur.executemany("INSERT OR REPLACE INTO courses VALUES (?, ?, ?, ?, ?)", courses)

conn.commit()
conn.close()
print("Setup complete")
