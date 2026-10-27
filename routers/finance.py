from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Finance, Student
from schemas import FinanceIn, FinanceOut
from decimal import Decimal

router = APIRouter(
    prefix="/finance",
    tags=["Finance Management"]
)

@router.post("/initialise", response_model= FinanceOut)
def initialize_fees(finance: FinanceIn, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == finance.student_id).first()
    if not student:
        raise HTTPException(status_code= 404, detail="Student does not exists")
    existing = db.query(Finance).filter(Finance.student_id == finance.student_id).first()
    if existing:
        raise HTTPException(status_code= 400, detail="Finance record already exists")
    new_record = Finance(**finance.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.patch("/update-record/{student_id}", response_model=FinanceOut)
def update_record(student_id: int, amount: Decimal, db: Session = Depends(get_db)):
    record = db.query(Finance).filter(Finance.student_id == student_id).first()
    if not record:
        raise HTTPException(status_code= 404, detail="No finance record exists")
    remaining_amount = record.total_fees-record.paid_amount
    if amount > remaining_amount:
        raise HTTPException(status_code= 400, detail=f"The required amount is {remaining_amount}, and you are paying {amount}")
    record.paid_amount += amount
    db.commit()
    db.refresh(record)
    return record