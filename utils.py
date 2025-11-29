from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError


# ---------------------------------------------------------
# Response Helpers (STRICT + CONSISTENT)
# ---------------------------------------------------------


def success_response(data=None, message=None, status=200):
    """
    Standard success format:
    {
        "success": true,
        "message": "...",
        "data": {...}
    }
    """
    payload = {"success": True}

    if message is not None:
        payload["message"] = message

    # Always include 'data' key for consistency.
    payload["data"] = data if data is not None else {}

    return jsonify(payload), status


def error_response(message, status=400):
    """
    Standard error format:
    {
        "success": false,
        "error": {
            "message": "...",
            "status": 400
        }
    }
    """
    return (
        jsonify(
            {
                "success": False,
                "error": {
                    "message": message,
                    "status": status,
                },
            }
        ),
        status,
    )


# ---------------------------------------------------------
# Validation Helper (STRICT)
# ---------------------------------------------------------


def validate_data(data, allowed_fields, required_fields=None):
    """
    Strict validation rules:

    1. Must be valid JSON dict.
    2. No unknown fields allowed.
    3. All required fields must be present.
    4. All provided fields must pass validators.

    allowed_fields:
        {
            "field_name": validator_function(value)
        }

    required_fields:
        ["field1", "field2"]
    """

    # Must be a JSON dict
    if not isinstance(data, dict):
        return False, "Invalid JSON payload, expected an object"

    # Reject unknown fields
    for key in data.keys():
        if key not in allowed_fields:
            return False, f"Unknown field: '{key}'"

    # Missing required fields
    if required_fields:
        missing = [field for field in required_fields if field not in data]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"

    # Validate each provided field
    for field, validator in allowed_fields.items():
        if field in data:
            if not validator(data[field]):
                return False, f"Invalid value for '{field}'"

    return True, None
