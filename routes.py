# routes.py
from flask import Blueprint, request, g
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Student
from utils import success_response, error_response, validate_data

student_bp = Blueprint("students", __name__, url_prefix="/students")

ALLOWED_FIELDS = {
    "name": lambda v: isinstance(v, str) and bool(v.strip()),
    "age": lambda v: isinstance(v, int) and v > 0,
}
REQUIRED_FIELDS = ["name", "age"]


@student_bp.post("/")
def create_student():
    data = request.get_json()
    valid, msg = validate_data(data, ALLOWED_FIELDS, REQUIRED_FIELDS)
    if not valid:
        return error_response(msg, 400)

    session = g.db
    try:
        student = Student(name=data["name"].strip(), age=data["age"])
        session.add(student)
        session.commit()
        session.refresh(student)
    except IntegrityError:
        session.rollback()
        return error_response("Student with this name and age already exists", 400)
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"DB error: {str(e)}", 500)

    return success_response(
        data=student.to_dict(), message="Student created", status=201
    )


@student_bp.get("/")
def get_students():
    session = g.db
    try:
        students = session.query(Student).all()
        return success_response(data=[s.to_dict() for s in students])
    except SQLAlchemyError as e:
        return error_response(f"DB error: {str(e)}", 500)


@student_bp.get("/<int:student_id>")
def get_student(student_id):
    session = g.db
    student = session.get(Student, student_id)
    if not student:
        return error_response("Student not found", 404)
    return success_response(data=student.to_dict())


@student_bp.get("/count")
def count_students():
    session = g.db
    try:
        count = session.query(Student).count()
        return success_response(data={"count": count})
    except SQLAlchemyError as e:
        return error_response(f"DB error: {str(e)}", 500)


@student_bp.put("/<int:student_id>")
def update_student(student_id):
    data = request.get_json()
    valid, msg = validate_data(data, ALLOWED_FIELDS, REQUIRED_FIELDS)
    if not valid:
        return error_response(msg, 400)

    session = g.db
    student = session.get(Student, student_id)
    if not student:
        return error_response("Student not found", 404)

    try:
        student.name = data["name"].strip()
        student.age = data["age"]
        session.commit()
        session.refresh(student)
    except IntegrityError:
        session.rollback()
        return error_response("Student with this name and age already exists", 400)
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"DB error: {str(e)}", 500)

    return success_response(
        data={"student": student.to_dict()}, message="Student updated"
    )


@student_bp.patch("/<int:student_id>")
def patch_student(student_id):
    data = request.get_json()
    valid, msg = validate_data(data, ALLOWED_FIELDS)
    if not valid:
        return error_response(msg, 400)

    if not data:
        # If client sends empty body intentionally, reject (strict behavior)
        return error_response("No updatable fields provided", 400)

    session = g.db
    student = session.get(Student, student_id)
    if not student:
        return error_response("Student not found", 404)

    if "name" in data:
        student.name = data["name"].strip()
    if "age" in data:
        student.age = data["age"]

    try:
        session.commit()
        session.refresh(student)
    except IntegrityError:
        session.rollback()
        return error_response("Student with this name and age already exists", 400)
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"DB error: {str(e)}", 500)

    return success_response(
        data={"student": student.to_dict()}, message="Student partially updated"
    )


@student_bp.delete("/<int:student_id>")
def delete_student(student_id):
    session = g.db
    student = session.get(Student, student_id)
    if not student:
        return error_response("Student not found", 404)

    try:
        session.delete(student)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"DB error: {str(e)}", 500)

    return success_response(data={}, message="Student deleted successfully")
