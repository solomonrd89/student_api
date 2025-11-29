# app.py
from flask import Flask, g
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
from routes import student_bp
from routes_course import course_bp
from utils import success_response, error_response

load_dotenv()


def get_engine():
    uri = os.getenv("DB_URI")
    if not uri:
        raise ValueError("DB_URI is missing in .env")
    return create_engine(uri, echo=True, future=True)


def create_app():
    app = Flask(__name__)

    # SQLAlchemy setup
    engine = get_engine()
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
    app.session_factory = scoped_session(SessionFactory)

    # DB session per request
    @app.before_request
    def create_session():
        g.db = app.session_factory()

    @app.teardown_request
    def remove_session(exception=None):
        db = g.get("db")
        if db:
            db.close()

    # Register blueprints
    app.register_blueprint(student_bp)
    app.register_blueprint(course_bp)

    # Root route (use strict success format)
    @app.get("/")
    def home():
        return success_response(
            data={"message": "Student & Course API is running"}, status=200
        )

    # Error handlers (use strict error format)
    @app.errorhandler(404)
    def not_found(_):
        return error_response("Resource not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(_):
        return error_response("Method not allowed", 405)

    @app.errorhandler(500)
    def internal_error(_):
        return error_response("Internal server error", 500)

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
