from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import io

import models, schemas
from database import engine, SessionLocal
from groq_ai import generate_insights

# Create tables
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ DB Connected")
except Exception as e:
    print("❌ DB Error:", str(e))

app = FastAPI()

# CORS (for Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def home():
    return {"message": "Student Analytics API 🚀"}

# -----------------------------
# Upload CSV
# -----------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(io.BytesIO(await file.read()))

    for _, row in df.iterrows():
        student = models.Student(**row.to_dict())
        db.add(student)

    db.commit()
    return {"message": "CSV uploaded successfully"}

# -----------------------------
# Add Student
# -----------------------------
@app.post("/students", response_model=schemas.StudentResponse)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# -----------------------------
# Update Student
# -----------------------------
@app.put("/students/{id}")
def update_student(id: int, data: schemas.StudentUpdate, db: Session = Depends(get_db)):

    student = db.query(models.Student).filter(models.Student.id == id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in data.dict().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student

# -----------------------------
# Get All Students
# -----------------------------
@app.get("/students", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# -----------------------------
# Analytics
# -----------------------------
@app.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()

    if not students:
        return {"message": "No data"}

    df = pd.DataFrame([s.__dict__ for s in students])

    return {
        "avg_cgpa": float(df["be_cgpa"].mean()),
        "placement_rate": float(df["placed"].mean() * 100),
        "top_students": df.sort_values("be_cgpa", ascending=False).head(5).to_dict(),
        "at_risk": df[df["be_cgpa"] < 6].to_dict()
    }

# -----------------------------
# AI Insights
# -----------------------------
@app.get("/ai")
def ai(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    data = [s.__dict__ for s in students]

    insights = generate_insights(data)

    return {"insights": insights}
