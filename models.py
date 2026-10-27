from sqlalchemy import  Column, Integer, String, ForeignKey, Boolean, Computed, Numeric
from sqlalchemy.orm import  relationship
from database import Base

class ClassRoom(Base):
    __tablename__= "classroom"

    id = Column(Integer, primary_key=True, index= True, unique= True)
    grade_name = Column(String)
    section = Column(String)
    students = relationship("Student", back_populates="class_link", cascade= "all, delete-orphan")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key= True, index= True, unique= True)
    roll_no = Column(Integer)
    name = Column(String)
    class_id = Column(Integer, ForeignKey("classroom.id"))
    class_link = relationship("ClassRoom", back_populates="students") 
    finances = relationship("Finance", back_populates="student_record")
    student_marks = relationship("Marks", back_populates="student")
    # this cascade is added to handle orphan child if a class is deleted
    # we could also use cascade="all, delete-orphan" if we want to atill save the orphan child in th database
    # but this what we used is used for deleting the orphans if the parent got deleted

class Finance(Base):
    __tablename__ = "finance_records"

    id = Column(Integer, primary_key= True, index= True, unique= True)
    student_id = Column(Integer, ForeignKey("students.id"))
    total_fees = Column(Numeric(10,2))
    paid_amount = Column(Numeric(10,2))
    is_cleared = Column(Boolean, Computed("paid_amount >= total_fees"))
    student_record = relationship("Student", back_populates="finances")

    
class Marks(Base):
    __tablename__ = "marks_records"

    id = Column(Integer, primary_key= True, index= True, unique= True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_name = Column(String)
    marks = Column(Numeric(10,2))
    student = relationship("Student", back_populates="student_marks")