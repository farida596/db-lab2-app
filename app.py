import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config["MYSQL_HOST"] = os.getenv("DB_HOST", "localhost")
app.config["MYSQL_USER"] = os.getenv("DB_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("DB_PASSWORD", "")
app.config["MYSQL_DB"] = os.getenv("DB_NAME", "registration")
app.secret_key = os.getenv("SESSION_SECRET", "super_secret_key")

mysql = MySQL(app)

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT todo_id, title, is_done FROM todos WHERE user_id = %s;",
        (user_id,)
    )
    todos = cursor.fetchall()
    cursor.close()
    
    # Format todos into a list of dictionaries for clean template usage
    todo_list = []
    for todo in todos:
        # Handle byte representation for is_done if applicable
        status = todo[2]
        if isinstance(status, bytes):
            status = int.from_bytes(status, byteorder='big')
            
        todo_list.append({
            "todo_id": todo[0],
            "title": todo[1],
            "is_done": status
        })
        
    return render_template("todos.html", todos=todo_list, name=session.get("user_name"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_id, name, password FROM users WHERE email = %s;", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid email or password")
            
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        hashed_password = generate_password_hash(password)
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s);",
                (name, email, hashed_password)
            )
            mysql.connection.commit()
        except Exception as e:
            cursor.close()
            return render_template("register.html", error="Email already registered or database error.")
        cursor.close()
        
        return redirect(url_for("login"))
        
    return render_template("register.html")

@app.route("/add", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    title = request.form.get("title")
    if title and title.strip():
        user_id = session["user_id"]
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO todos (user_id, title, is_done) VALUES (%s, %s, 0);",
            (user_id, title.strip())
        )
        mysql.connection.commit()
        cursor.close()
        
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>", methods=["POST"])
def update_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    cursor = mysql.connection.cursor()
    
    # Fetch the current task status
    cursor.execute(
        "SELECT is_done FROM todos WHERE todo_id = %s AND user_id = %s;",
        (todo_id, user_id)
    )
    todo = cursor.fetchone()
    
    if todo:
        # Safely handle whether the cursor returns a tuple or a dictionary
        if isinstance(todo, dict):
            current_status = todo['is_done']
        else:
            current_status = todo[0]
            
        # Handle potential byte values from MySQL TINYINT
        if isinstance(current_status, bytes):
            current_status = int.from_bytes(current_status, byteorder='big')
            
        # Toggle: if 1, make it 0; otherwise make it 1
        new_status = 0 if current_status else 1
        
        # Update the database
        cursor.execute(
            "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s;",
            (new_status, todo_id, user_id)
        )
        mysql.connection.commit()
        
    cursor.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    user_id = session["user_id"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        "DELETE FROM todos WHERE todo_id = %s AND user_id = %s;",
        (todo_id, user_id)
    )
    mysql.connection.commit()
    cursor.close()
    
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)