from pydantic import BaseModel, Field
from typing import Optional

class StudentBase(BaseModel):
    name: str = Field(..., min_length=2)

    tenth: float = Field(..., ge=0, le=100)
    twelfth: float = Field(..., ge=0, le=100)
    be_cgpa: float = Field(..., ge=0, le=10)

    skills: str
    domain: str

    projects: int = Field(..., ge=0)
    hackathons: int = Field(..., ge=0)
    papers: int = Field(..., ge=0)

    placed: bool

    company: Optional[str] = None
    salary: Optional[float] = None
    company_type: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True
