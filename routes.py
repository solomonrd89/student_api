from flask import Blueprint, request, jsonify

student_bp = Blueprint("students", __name__, url_prefix="/students")

# ----------------------------------------------------
# In-memory database (temporary)
# ----------------------------------------------------
students = []
next_id = 1


# ----------------------------------------------------
# Response Helpers (consistent across all routes)
# ----------------------------------------------------
def success_response(data, status=200):
    return jsonify({"success": True, "data": data}), status


def error_response(message, status=400):
    return (
        jsonify({"success": False, "error": {"message": message, "status": status}}),
        status,
    )


# ----------------------------------------------------
# Utilities
# ----------------------------------------------------
def find_student(student_id: int):
    """Return student dict or None."""
    return next((s for s in students if s["id"] == student_id), None)


def validate_student_data(data, required_fields=None):
    """
    Validate JSON input.
    - required_fields={"name", "age"} → strict check for PUT
    - None → PATCH validation (soft)
    """
    if not data:
        return False, "JSON body is required"

    allowed_fields = {"name", "age"}
    unknown = set(data.keys()) - allowed_fields
    if unknown:
        return False, f"Invalid fields: {', '.join(unknown)}"

    # Strict validation for PUT
    if required_fields:
        if set(data.keys()) != required_fields:
            return False, "Both 'name' and 'age' are required"

    # Field validation
    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return False, "Valid 'name' (string) is required"

    if "age" in data:
        if not isinstance(data["age"], int):
            return False, "Valid 'age' (int) is required"

    return True, None


# ----------------------------------------------------
# POST /students
# ----------------------------------------------------
@student_bp.post("/")
def create_student():
    global next_id
    data = request.get_json()

    valid, msg = validate_student_data(data, required_fields={"name", "age"})
    if not valid:
        return error_response(msg, 400)

    student = {
        "id": next_id,
        "name": data["name"].strip(),
        "age": data["age"],
    }

    students.append(student)
    next_id += 1

    return success_response(student, 201)


# ----------------------------------------------------
# GET /students
# ----------------------------------------------------
@student_bp.get("/")
def get_students():
    return success_response(students)


# ----------------------------------------------------
# GET /students/<id>
# ----------------------------------------------------
@student_bp.get("/<int:student_id>")
def get_student(student_id):
    student = find_student(student_id)
    if not student:
        return error_response("Student not found", 404)

    return success_response(student)


# ----------------------------------------------------
# GET /students/count
# ----------------------------------------------------
@student_bp.get("/count")
def count_students():
    return success_response({"count": len(students)})


# ----------------------------------------------------
# PUT /students/<id>
# ----------------------------------------------------
@student_bp.put("/<int:student_id>")
def update_student(student_id):
    student = find_student(student_id)
    if not student:
        return error_response("Student not found", 404)

    data = request.get_json()
    valid, msg = validate_student_data(data, required_fields={"name", "age"})
    if not valid:
        return error_response(msg, 400)

    student["name"] = data["name"].strip()
    student["age"] = data["age"]

    return success_response(
        {"message": "Student updated successfully", "student": student}
    )


# ----------------------------------------------------
# PATCH /students/<id>
# ----------------------------------------------------
@student_bp.patch("/<int:student_id>")
def patch_student(student_id):
    student = find_student(student_id)
    if not student:
        return error_response("Student not found", 404)

    data = request.get_json()
    valid, msg = validate_student_data(data)
    if not valid:
        return error_response(msg, 400)

    if "name" in data:
        student["name"] = data["name"].strip()
    if "age" in data:
        student["age"] = data["age"]

    return success_response(
        {"message": "Student partially updated", "student": student}
    )


# ----------------------------------------------------
# DELETE /students/<id>
# ----------------------------------------------------
@student_bp.delete("/<int:student_id>")
def delete_student(student_id):
    global students

    student = find_student(student_id)
    if not student:
        return error_response("Student not found", 404)

    students = [s for s in students if s["id"] != student_id]

    return success_response(
        {"message": "Student deleted successfully", "student": student}
    )
