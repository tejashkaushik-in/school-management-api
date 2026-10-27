from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class CreateClass(BaseModel):
    id : int
    grade_name : str
    section : str

class ClassOut(BaseModel):
    grade_name : str
    section : str
    class Config:
        from_attributes = True

class StudentIn(BaseModel):
    id : int
    roll_no : int
    name : str
    class_id : int

class StudentOut(BaseModel):
    name : str
    roll_no : int
    class_link : Optional[ClassOut]
    class Config:
        from_attributes = True

class ClassWithStudents(BaseModel):
    grade_name : str
    section : str
    students : list[StudentOut]
    class Config:
        from_attributes = True

class FinanceIn(BaseModel):
    id : int
    student_id : int
    total_fees : Decimal
    paid_amount : Decimal = 0.0

class FinanceOut(BaseModel):
    id : int
    total_fees : Decimal
    paid_amount : Decimal
    is_cleared : bool
    class Config:
        from_attributes = True

class MarksIn(BaseModel):
    id : int
    student_id : int
    subject_name : str
    marks : Decimal = Field(ge = 0, le= 100)
    
class StudentFiltered(BaseModel):
    roll_no : int
    name : str
    class Config:
        from_attributes = True

class MarksOut(BaseModel):
    student : Optional[StudentFiltered]
    subject_name : str
    marks : Decimal 
    class Config:
        from_attributes = True