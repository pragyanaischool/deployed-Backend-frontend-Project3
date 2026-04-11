from pydantic import BaseModel
from typing import Optional

# Base schema
class StudentBase(BaseModel):
    name: str
    tenth: float
    twelfth: float
    be_cgpa: float
    skills: str
    domain: str
    projects: int
    hackathons: int
    papers: int
    placed: bool
    company: Optional[str] = None
    salary: Optional[float] = None
    company_type: Optional[str] = None

# Create
class StudentCreate(StudentBase):
    pass

# Update
class StudentUpdate(StudentBase):
    pass

# Response
class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
