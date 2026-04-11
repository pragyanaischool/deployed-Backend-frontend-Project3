from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import io

import models, schemas
from database import engine, SessionLocal
from groq_ai import generate_insights

# -----------------------------
# INIT DB
# -----------------------------
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database Connected")
except Exception as e:
    print("❌ DB Error:", str(e))

# -----------------------------
# INIT APP
# -----------------------------
app = FastAPI(
    title="Student Analytics API",
    version="2.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# DB DEPENDENCY
# -----------------------------
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
    return {"message": "🚀 Student Analytics API Running"}

# -----------------------------
# CSV UPLOAD (SAFE)
# -----------------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(io.BytesIO(await file.read()))

        required_cols = [
            "name", "tenth", "twelfth", "be_cgpa",
            "skills", "domain", "projects",
            "hackathons", "papers", "placed"
        ]

        for col in required_cols:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing column: {col}")

        for _, row in df.iterrows():
            student = models.Student(**row.to_dict())
            db.add(student)

        db.commit()

        return {"message": f"{len(df)} records inserted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# ADD STUDENT
# -----------------------------
@app.post("/students", response_model=schemas.StudentResponse)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):

    new_student = models.Student(**student.dict())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

# -----------------------------
# UPDATE STUDENT
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
# GET STUDENTS
# -----------------------------
@app.get("/students", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

# -----------------------------
# ANALYTICS ENGINE
# -----------------------------
@app.get("/analytics")
def analytics(db: Session = Depends(get_db)):

    students = db.query(models.Student).all()

    if not students:
        return {"message": "No data available"}

    df = pd.DataFrame([s.__dict__ for s in students])

    return {
        "avg_cgpa": float(df["be_cgpa"].mean()),
        "placement_rate": float(df["placed"].mean() * 100),
        "top_students": df.sort_values("be_cgpa", ascending=False).head(5).to_dict(),
        "at_risk_students": df[df["be_cgpa"] < 6].to_dict(),
        "avg_projects": float(df["projects"].mean())
    }

# -----------------------------
# AI INSIGHTS
# -----------------------------
@app.get("/ai-insights")
def ai_insights(db: Session = Depends(get_db)):

    students = db.query(models.Student).all()

    if not students:
        return {"message": "No data available"}

    data = [
        {
            "name": s.name,
            "cgpa": s.be_cgpa,
            "skills": s.skills,
            "projects": s.projects,
            "placed": s.placed
        }
        for s in students
    ]

    insights = generate_insights(data)

    return {"insights": insights}
