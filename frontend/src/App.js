import React, { useState } from "react";
import axios from "axios";

function App() {
    const [code, setCode] = useState("");
    const [course, setCourse] = useState(null);
    const [error, setError] = useState("");

    const fetchCourse = async () => {
        try {
            const res = await axios.get(`http://localhost:8000/api/course/${code}`);
            setCourse(res.data);
            setError("");
        } catch (e) {
            setCourse(null);
            setError("Course not found!");
        }
    }

    return (
        <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "Arial, sans-serif" }}>
            <h1>UQ Course Lookup</h1>
            <input
                type="text"
                placeholder="Enter course code"
                value={code}
                onChange={(e) => setCode(e.target.value.toUpperCase())}
                onKeyDown={(e) => e.key === "Enter" && fetchCourse()}
                style={{ width: "100%", padding: "10px", fontSize: "16px" }}
            />
            <button onClick={fetchCourse} style={{ marginTop: "10px" }}>
                Search
            </button>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {course && (
                <div style={{ marginTop: "20px", backgroundColor: "#f9f9f9", padding: "15px", borderRadius: "8px" }}>
                    <p><strong>Course Code:</strong> {code}</p>
                    <p><strong>Title:</strong> {course.title}</p>
                    <p><strong>Description:</strong> {course.description}</p>
                    <p><strong>Prerequisites:</strong> {course.prerequisites || "None"}</p>
                    <p><strong>Incompatible:</strong> {course.incompatible || "None"}</p>
                </div>
            )}
        </div>
    );
}

export default App;
