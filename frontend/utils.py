import requests
from config import API_URL

# -----------------------------
# Upload CSV
# -----------------------------
def upload_csv(file):
    return requests.post(
        f"{API_URL}/upload",
        files={"file": file}
    )

# -----------------------------
# Get Students
# -----------------------------
def get_students():
    return requests.get(f"{API_URL}/students")

# -----------------------------
# Add Student
# -----------------------------
def add_student(data):
    return requests.post(f"{API_URL}/students", json=data)

# -----------------------------
# Update Student
# -----------------------------
def update_student(student_id, data):
    return requests.put(f"{API_URL}/students/{student_id}", json=data)

# -----------------------------
# Analytics
# -----------------------------
def get_analytics():
    return requests.get(f"{API_URL}/analytics")

# -----------------------------
# AI Insights
# -----------------------------
def get_ai_insights():
    return requests.get(f"{API_URL}/ai-insights")
