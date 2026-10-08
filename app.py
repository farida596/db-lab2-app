import os
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET")

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("todo_list"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            flash("All fields are required", "register_error")
            return render_template("register.html")
        if password != confirm_password:
            flash("Passwords do not match", "register_error")
            return render_template("register.html")

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s);"
                cursor.execute(query, (email, name, hashed_pw))
                connection.commit()
                session["user_id"] = cursor.lastrowid
                session["user_name"] = name
                return redirect(url_for("todo_list"))
        except pymysql.err.IntegrityError:
            flash("Email Already Exists", "register_error")
            return render_template("register.html")
        finally:
            connection.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required", "login_error")
            return render_template("login.html")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                query = "SELECT user_id, name, password_hash FROM users WHERE email = %s;"
                cursor.execute(query, (email,))
                user = cursor.fetchone()

                if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
                    session["user_id"] = user["user_id"]
                    session["user_name"] = user["name"]
                    return redirect(url_for("todo_list"))
                else:
                    flash("Invalid email or password", "login_error")
        finally:
            connection.close()
        return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/todos")
def todo_list():
    if "user_id" not in session:
        return redirect(url_for("login"))
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC;"
            cursor.execute(query, (session["user_id"],))
            todos = cursor.fetchall()
    finally:
        connection.close()
    return render_template("todos.html", todos=todos, name=session["user_name"])

@app.route("/todos/add", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    title = request.form.get("title", "").strip()
    if not title:
        flash("Title is required", "todo_error")
    elif len(title) > 200:
        flash("Title is too long (200 characters at most)", "todo_error")
    else:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO todos (user_id, title) VALUES (%s, %s);"
                cursor.execute(query, (session["user_id"], title))
                connection.commit()
        finally:
            connection.close()
    return redirect(url_for("todo_list"))

@app.route("/todos/update/<int:todo_id>", methods=["POST"])
def update_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    title = request.form.get("title", "").strip()
    is_done = 1 if request.form.get("is_done") == "on" else 0
    if not title:
        flash("Title is required", "todo_error")
    elif len(title) > 200:
        flash("Title is too long (200 characters at most)", "todo_error")
    else:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                query = "UPDATE todos SET title = %s, is_done = %s WHERE todo_id = %s AND user_id = %s;"
                cursor.execute(query, (title, is_done, todo_id, session["user_id"]))
                connection.commit()
        finally:
            connection.close()
    return redirect(url_for("todo_list"))

@app.route("/todos/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM todos WHERE todo_id = %s AND user_id = %s;"
            cursor.execute(query, (todo_id, session["user_id"]))
            connection.commit()
    finally:
        connection.close()
    return redirect(url_for("todo_list"))

if __name__ == "__main__":
    app.run(debug=True)
