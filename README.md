# Student API

A minimal REST API built with **Flask**. Manages an in-memory list of students with full CRUD operations, input validation, and standardized JSON responses.

---

## Features

* Organized with **Blueprints**
* Standardized JSON responses
* Full CRUD: POST, GET, PUT, PATCH, DELETE
* Input validation for fields and types
* Global error handling: 404, 405, 500
* `.env` support via **python-dotenv**

---

## Project Structure

```
student_api/
│── venv/
│── app.py
│── routes.py
│── requirements.txt
│── .env
│── README.md
```

---

## Setup

1. **Create & activate virtual environment**

```bash
python -m venv venv
venv/Scripts/activate   # Windows
source venv/bin/activate  # macOS/Linux
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Create `.env`**

```
PORT=5000
FLASK_ENV=development
```

4. **Run the server**

```bash
python app.py
```

Server: `http://127.0.0.1:5000`

---

## Base URL

```
/students
```

---

## API Endpoints

| Method | Endpoint        | Description            |
| ------ | --------------- | ---------------------- |
| GET    | /               | Health check           |
| POST   | /students       | Create student         |
| GET    | /students       | Get all students       |
| GET    | /students/<id>  | Get student by ID      |
| GET    | /students/count | Count students         |
| PUT    | /students/<id>  | Full update student    |
| PATCH  | /students/<id>  | Partial update student |
| DELETE | /students/<id>  | Delete student         |

### Response Format

* **Success**

```json
{
  "success": true,
  "data": { ... }
}
```

* **Error**

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "status": 400
  }
}
```

---

## Testing

Use Postman, Thunder Client, cURL, or browser (GET only).

---
