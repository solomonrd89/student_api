# routes_course.py
from flask import Blueprint, request, g
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Course
from utils import success_response, error_response, validate_data

course_bp = Blueprint("courses", __name__, url_prefix="/courses")

ALLOWED_FIELDS = {
    "title": lambda v: isinstance(v, str) and bool(v.strip()),
    "credits": lambda v: isinstance(v, int) and v > 0,
}
REQUIRED_FIELDS = ["title", "credits"]


@course_bp.post("/")
def create_course():
    data = request.get_json()
    valid, msg = validate_data(data, ALLOWED_FIELDS, REQUIRED_FIELDS)
    if not valid:
        return error_response(msg, 400)

    session = g.db
    try:
        course = Course(title=data["title"].strip(), credits=data["credits"])
        session.add(course)
        session.commit()
        session.refresh(course)
    except IntegrityError:
        session.rollback()
        return error_response("Course with this title already exists", 400)
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"DB error: {str(e)}", 500)

    return success_response(data=course.to_dict(), message="Course created", status=201)


@course_bp.get("/")
def get_courses():
    session = g.db
    try:
        courses = session.query(Course).all()
        return success_response(data=[c.to_dict() for c in courses])
    except SQLAlchemyError as e:
        return error_response(f"DB error: {str(e)}", 500)


@course_bp.get("/<int:course_id>")
def get_course(course_id):
    session = g.db
    course = session.get(Course, course_id)
    if not course:
        return error_response("Course not found", 404)
    return success_response(data=course.to_dict())


@course_bp.get("/count")
def count_courses():
    session = g.db
    try:
        count = session.query(Course).count()
        return success_response(data={"count": count})
    except SQLAlchemyError as e:
        return error_response(f"DB error: {str(e)}", 500)


@course_bp.put("/<int:course_id>")
def update_course(course_id):
    data = request.get_json()
    valid, msg = validate_data(data, ALLOWED_FIELDS, REQUIRED_FIELDS)
    if not valid:
        return error_response(msg, 400)

    session = g.db
    course = session.get(Course, course_id)
    if not course:
        return error_response("Course not found", 404)

    try:
        course.title = data["title"].strip()
        course.credits = data["credits"]
        session.commit()
        session.refresh(course)
    except IntegrityError:
        session.rollback()
        return error_response("Course with this title already exists", 400)
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"DB error: {str(e)}", 500)

    return success_response(data={"course": course.to_dict()}, message="Course updated")


@course_bp.patch("/<int:course_id>")
def patch_course(course_id):
    data = request.get_json()
    valid, msg = validate_data(data, ALLOWED_FIELDS)
    if not valid:
        return error_response(msg, 400)

    if not data:
        return error_response("No updatable fields provided", 400)

    session = g.db
    course = session.get(Course, course_id)
    if not course:
        return error_response("Course not found", 404)

    if "title" in data:
        course.title = data["title"].strip()
    if "credits" in data:
        course.credits = data["credits"]

    try:
        session.commit()
        session.refresh(course)
    except IntegrityError:
        session.rollback()
        return error_response("Course with this title already exists", 400)
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"DB error: {str(e)}", 500)

    return success_response(
        data={"course": course.to_dict()}, message="Course partially updated"
    )


@course_bp.delete("/<int:course_id>")
def delete_course(course_id):
    session = g.db
    course = session.get(Course, course_id)
    if not course:
        return error_response("Course not found", 404)

    try:
        session.delete(course)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"DB error: {str(e)}", 500)

    return success_response(data={}, message="Course deleted successfully")
