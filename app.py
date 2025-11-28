from flask import Flask, jsonify
from dotenv import load_dotenv
import os

load_dotenv()


# ----------------------------------------------------
# Factory Function: Creates and configures the Flask app
# ----------------------------------------------------
def create_app():
    app = Flask(__name__)

    # ----------------------------------------------------
    # Register Blueprints
    # ----------------------------------------------------
    from routes import student_bp

    app.register_blueprint(student_bp)

    # ----------------------------------------------------
    # Health & Root Route
    # ----------------------------------------------------
    @app.get("/")
    def home():
        return (
            jsonify({"success": True, "data": {"message": "Student API is running"}}),
            200,
        )

    # ----------------------------------------------------
    # Global Error Handlers
    # ----------------------------------------------------
    @app.errorhandler(404)
    def not_found(_):
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "message": "Resource not found",
                        "status": 404,
                    },
                }
            ),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(_):
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "message": "Method not allowed",
                        "status": 405,
                    },
                }
            ),
            405,
        )

    @app.errorhandler(500)
    def internal_error(_):
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "message": "Internal server error",
                        "status": 500,
                    },
                }
            ),
            500,
        )

    return app


# ----------------------------------------------------
# Application Entry Point
# ----------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))

    # Production-safe: Explicit host, explicit port
    # Debug only enabled when FLASK_ENV=development
    debug_mode = os.getenv("FLASK_ENV", "production") == "development"

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
