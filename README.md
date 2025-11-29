# 🚀 Student & Course API
A production-grade REST API built with **Flask**, **SQLAlchemy**, and **MySQL** — featuring strict validation, consistent JSON responses, and clean architecture.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue" />
  <img src="https://img.shields.io/badge/Flask-2.x-lightgrey" />
  <img src="https://img.shields.io/badge/SQLAlchemy-2.x-red" />
  <img src="https://img.shields.io/badge/MySQL-8.0-blue" />
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen" />
</p>

---
# 📘 Overview
A clean, strict, and scalable backend API for managing **Students** and **Courses**, using:
- Flask blueprints
- SQLAlchemy ORM (2.x)
- Strict input validation
- MySQL engine
- Professional project layout

Perfect for learning real-world backend practices.

---
# 📁 Project Structure
```
student_api/
│   app.py
│   models.py
│   routes.py
│   routes_course.py
│   utils.py
│   .env
│   requirements.txt
│   README.md
```

---
# ⚙️ Installation & Setup
## 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/student_api.git
cd student_api
```
## 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```
## 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```
## 4️⃣ Configure .env
```
FLASK_ENV=development
PORT=5000
DB_URI=mysql+pymysql://root:YOURPASSWORD@localhost:3306/student_api
```
## 5️⃣ Run Server
```bash
python app.py
```

---
# 📡 API Response Format (STRICT)
### ✔ Success
```json
{
  "success": true,
  "message": "optional",
  "data": {}
}
```
### ❌ Error
```json
{
  "success": false,
  "error": {
    "message": "What went wrong",
    "status": 400
  }
}
```

---
# 🛠 Students API
| Method | Route | Description |
|--------|--------|-------------|
| POST   | /students/ | Create student |
| GET    | /students/ | Get all students |
| GET    | /students/<id> | Get one student |
| GET    | /students/count | Count students |
| PUT    | /students/<id> | Update student |
| PATCH  | /students/<id> | Partially update student |
| DELETE | /students/<id> | Delete student |

---
# 📘 Courses API
| Method | Route | Description |
|--------|--------|-------------|
| POST   | /courses/ | Create course |
| GET    | /courses/ | Get all courses |
| GET    | /courses/<id> | Get one course |
| GET    | /courses/count | Count courses |
| PUT    | /courses/<id> | Update course |
| PATCH  | /courses/<id> | Partially update course |
| DELETE | /courses/<id> | Delete course |

---
# 🧪 Example Request
### Create Student
```bash
curl -X POST http://localhost:5000/students/ \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "age": 20}'
```

---
# 🔍 Validation Rules
### Students
| Field | Type | Rule |
|--------|--------|------|
| name | string | required, non-empty |
| age | int | required, > 0 |

### Courses
| Field | Type | Rule |
|--------|--------|------|
| title | string | required, non-empty |
| credits | int | required, > 0 |

Strict mode:
- Unknown fields → ❌ error
- Wrong type → ❌ error
- Missing required → ❌ error

---
# 🛢 Database Schema
### Students Table
| Column | Type |
|---------|---------|
| id | int (PK, auto increment) |
| name | varchar(100) |
| age | int |
| UNIQUE(name, age) |

### Courses Table
| Column | Type |
|---------|---------|
| id | int (PK, auto increment) |
| title | varchar(100) |
| credits | int |
| UNIQUE(title) |

---
# 🚀 Deployment Guide (Production)
### Gunicorn + Nginx
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app
```
### Dockerfile
```Dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---
# 📤 Push to GitHub
```bash
git add .
git commit -m "Updated production README"
git push origin main
```

---
# ✅ Status
Your API is complete, strict, production-ready, documented, and GitHub‑optimized.

