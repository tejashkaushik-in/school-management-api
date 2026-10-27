from fastapi import FastAPI
from database import engine, Base
from routers import students, classrooms, finance, marks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Management System")

app.include_router(students.router)
app.include_router(classrooms.router)
app.include_router(finance.router)
app.include_router(marks.router)

@app.get("/")
def home():
    return {"message": "Welcome to the School Management System"}