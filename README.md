# School Management System (RESTful API Backend)

A modular, relational school administration backend API built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**. The platform provides dedicated service routers for managing classroom capacities, student enrollment, academic grading registers, and student financial clearance workflows.

---

## Architectural Highlights

- **Relational Integrity & Cascades:** Structured relational mappings (\ClassRoom\, \Student\, \Finance\, \Marks\) enforcing foreign keys with automated \all, delete-orphan\ cascade deletion on dependent records.
- **Computed Financial Ledger:** Implemented real-time fee tracking with PostgreSQL computed columns evaluating clearance thresholds (\paid_amount >= total_fees\).
- **Capacity Constraint Engine:** Enforces business logic limits (maximum 5 students per classroom) directly within service routing boundaries.
- **Strict Data Sanitization:** Pydantic v2 schemas leveraging boundary validators (\ge=0, le=100\ on marks), decimal precision for financial deltas, and attribute mapping.

---

## Tech Stack

- **Framework:** FastAPI, Starlette, Pydantic v2
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0
- **Driver:** \psycopg2-binary\

---

## API Endpoints

### Classrooms (\/classrooms\)
- \POST /classrooms/add-class\ - Registers a grade level and section.
- \GET /classrooms/student-in-class?class_id={id}\ - Fetches classroom metadata along with nested student manifests.
- \DELETE /classrooms/delete-class/{class_id}\ - Deletes a classroom and cascades deletion to associated student records.

### Students (\/students\)
- \POST /students/add-student\ - Enrolls a student while validating classroom capacity quotas (max 5).
- \GET /students/student-by-id/{student_id}\ - Fetches individual student profile with assigned classroom metadata.
- \GET /students/students-by-name?name={name}\ - Case-insensitive student search.
- \PATCH /students/update-student/{student_id}\ - Updates student details and re-validates class transfer capacity.
- \DELETE /students/delete-student/{student_id}\ - Removes a student record.

### Finance (\/finance\)
- \POST /finance/initialise\ - Establishes tuition ledger records for enrolled students.
- \PATCH /finance/update-record/{student_id}\ - Records payment installments with overpayment validation checks.

### Marks Register (\/marks\)
- \POST /marks/add-marks\ - Records subject scores with strict boundary checks (0-100).
- \GET /marks/get-marks/{student_id}\ - Calculates GPA metrics, average score across subjects, and pass/fail thresholds (pass mark: 33).

---

## Getting Started Locally

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/tejashkaushik-in/<YOUR-REPO-NAME>.git
cd <YOUR-REPO-NAME>

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy \.env.example\ to \.env\ and verify database credentials:
```bash
cp .env.example .env
```

### 3. Run Application
```bash
uvicorn main:app --reload
```

Interactive API documentation will be available at:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
