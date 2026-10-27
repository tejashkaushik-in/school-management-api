from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Marks
from schemas import MarksIn, MarksOut
from decimal import Decimal

router = APIRouter(
    prefix = "/marks",
    tags =["Marks Register"]
)

@router.post("/add-marks", response_model=MarksOut)
def add_marks(marks: MarksIn, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == marks.student_id).first()
    if not student:
        raise HTTPException(status_code= 404, detail="No student exists")
    new_marks = Marks(**marks.model_dump())
    db.add(new_marks)
    db.commit()
    db.refresh(new_marks)
    return new_marks

@router.get("/get-marks/{student_id}")
def get_marks(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code= 404, detail=f"No student exists with {student_id} id")
    
    marks_list = student.student_marks

    if not marks_list:
        raise HTTPException(status_code= 404, detail="No record found")
    
    total_marks = sum(m.marks for m in marks_list)
    average = total_marks/len(marks_list)

    return {"student_name" : student.name,
            "total_subjects": len(marks_list),
            "average_score" : average,
            "status" : "Pass" if average >=33 else "Fail"
            }
