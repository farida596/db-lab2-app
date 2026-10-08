# Secure Flask Login & To-Do Application (Lab 2)

A robust full-stack web application built with **Python (Flask)** and **MySQL** featuring secure user authentication, password hashing, session management, and personalized task management (CRUD).

---

## 🚀 Tech Stack
* **Backend**: Python, Flask, PyMySQL
* **Security**: `bcrypt` (password hashing), Parameterized Queries (SQL injection prevention)
* **Database**: MySQL
* **Frontend**: HTML5, CSS3, Jinja2 Templates

---

## ✨ Key Features
* **User Authentication**: Secure registration and login system with encrypted password hashing.
* **Session Management**: Private user sessions ensuring users can only access and modify their own tasks.
* **To-Do CRUD Operations**: Add new tasks, update descriptions, check off completed items, and delete tasks.
* **Security Best Practices**: Guarded against SQL injection using parameterized inputs.

---

## 📁 Project Structure
```text
db-lab2-app/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── database/
│   └── schema.sql
├── static/
│   └── style.css
└── templates/
    ├── login.html
    ├── register.html
    └── todos.html
