from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import  ClassRoom
from schemas import  StudentOut, ClassOut, ClassWithStudents, CreateClass

router = APIRouter(
    prefix="/classrooms",    # All routes start with /students
    tags=["Classroom"]      # Groups them in Swagger UI
)


@router.post("/add-class", response_model=ClassOut)
def add_class(classroom: CreateClass, db :Session = Depends(get_db)):
    existing_class = db.query(ClassRoom).filter(ClassRoom.id == classroom.id).first()
    if existing_class:
        raise HTTPException(status_code= 400, detail="Classroom already exists")
    new_class = ClassRoom(
        id = classroom.id,
        grade_name = classroom.grade_name,
        section = classroom.section
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@router.get("/student-in-class", response_model= ClassWithStudents)
def student_in_class(class_id: int, db : Session = Depends(get_db)):
    existing_class = db.query(ClassRoom).filter(ClassRoom.id == class_id).first()
    if not existing_class:
        raise HTTPException(status_code= 404, detail="No class with this id exists")
    return existing_class

@router.delete("/delete-class/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    existing_class = db.query(ClassRoom).filter(ClassRoom.id == class_id).first()
    if not existing_class:
        raise HTTPException(status_code= 404, detail="No classroom found with this id")
    ID = existing_class.id
    db.delete(existing_class)
    db.commit()
    return {"message":f"Class {ID} deleted succesfully"}