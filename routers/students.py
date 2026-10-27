from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student, ClassRoom
from schemas import StudentIn, StudentOut

router = APIRouter(
    prefix="/students",    # All routes start with /students
    tags=["Students"]      # Groups them in Swagger UI
)


@router.post("/add-student", response_model= StudentOut)
def add_student(student: StudentIn, db: Session = Depends(get_db)):
    existing_class = db.query(ClassRoom).filter(ClassRoom.id == student.class_id).first()
    if not existing_class:
        raise HTTPException(status_code= 404, detail="No classroom found, create a classroom first")
    existing_student = db.query(Student).filter(Student.id == student.id).first()
    if existing_student:
        raise HTTPException(status_code= 400, detail="Student already exists")
    occupancy = db.query(Student).filter(Student.class_id == student.class_id).count()
    if occupancy >=5:
        raise HTTPException(status_code= 400, detail="Classroom is full! Maximum 5 students allowed.")
    new_student = Student(
        id = student.id,
        roll_no = student.roll_no,
        name = student.name,
        class_id = student.class_id
        )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/student-by-id/{student_id}", response_model= StudentOut)
def student_by_id(student_id : int, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(Student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code= 404, detail="No student found")
    return existing_student

@router.get("/students-by-name", response_model= list[StudentOut])
def student_by_name(name: str, db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.name.ilike(f"%{name}%")).all()
    if not students:
        raise HTTPException(status_code = 404, detail="No student found with that name")
    return students

@router.patch("/update-student/{student_id}", response_model= StudentOut)
def update_student(student_id: int, name: str = None, roll_no: int = None, class_id: int = None,db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code= 404, detail="No student found with this id")
    if name:
        student.name = name
    if roll_no:
        student.roll_no = roll_no
    if class_id:
        target_class = db.query(ClassRoom).filter(ClassRoom.id == class_id).first()
        if not target_class:
            raise HTTPException(status_code= 404, detail="No such classroom available")
        occupancy = db.query(Student).filter(Student.class_id == class_id).count()
        if occupancy >=5:
            raise HTTPException(status_code= 400, detail="Classroom is full! Maximum 5 students allowed.")
        student.class_id = class_id
    db.commit()
    db.refresh(student)
    return student

@router.delete("/delete-student/{student_id}")
def delete_student(student_id : int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code= 404, detail="No student found with this id")
    ID = student.id
    db.delete(student)
    db.commit()
    return{"message":f"Student {ID} deleted successfully"}