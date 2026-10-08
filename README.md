# Login & To-Do Application

A full-stack Login & To-Do web application developed for Database Systems Lab 2.

The application allows users to register, log in securely, and manage their own to-do items. Each user can only access and modify their own tasks.

---

## 1. Team Members

| Name           | Student ID | Responsibilities                                                                                                                  |
| -------------- | ---------: | --------------------------------------------------------------------------------------------------------------------------------- |
| Farida Mohamed |    2304245 | Database design, backend development, authentication, to-do functionality, validation, UI integration, testing, and documentation |

This project was completed individually.

---

## 2. Technologies Used

### Backend

* Python
* Flask
* PyMySQL
* bcrypt
* python-dotenv

### Frontend

* HTML
* CSS
* Jinja2 templates

### Database

* MySQL

---

## 3. Project Structure

```text
project-root/
│
├── database/
│   └── schema.sql
│
├── screenshots/
│   ├── login page.png
│   ├── one marked as done.png
│   ├── phone screenshot.png
│   └── register page error.png
│
├── static/
│   └── style.css
│
├── templates/
│   └── HTML/Jinja2 templates
│
├── .env.example
├── .gitignore
├── README.md
├── app.py
├── requirements.txt
└── setup.py
```

The `.env` file is intentionally not included in the repository because it contains private database credentials.

---

## 4. How to Run the Project

### Step 1 — Install Python

Make sure Python is installed on the machine.

Check:

```bash
python --version
```

---

### Step 2 — Install the Required Packages

From the project root:

```bash
pip install -r requirements.txt
```

---

### Step 3 — Set Up MySQL

Create the required database by running:

```bash
mysql -u root -p < database/schema.sql
```

The schema creates the required `users` and `todos` tables.

---

### Step 4 — Configure Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```bash
cp .env.example .env
```

On Windows, you can simply copy `.env.example` and rename the copy to:

```text
.env
```

Then configure the database connection values inside `.env`.

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_database_password
DB_NAME=registration
SESSION_SECRET=your_secret_key
```

Do not commit the real `.env` file to GitHub.

---

### Step 5 — Run the Application

Run:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

# 5. Features Implemented

## R1 — User Registration

Users can create an account using:

* Name
* Email
* Password
* Password confirmation

The application validates the required fields before creating the account.

Passwords are securely hashed using bcrypt before being stored in the database.

---

## R2 — Registration Validation

The application handles invalid registration input, including:

* Empty fields
* Password confirmation mismatch
* Duplicate email addresses

For duplicate emails, the application displays:

```text
Email Already Exists
```

---

## R3 — User Login

Registered users can log in using their:

* Email
* Password

The application verifies the password against the stored bcrypt password hash.

If the credentials are incorrect, the application displays:

```text
Invalid email or password
```

The same message is used for an unknown email or incorrect password.

---

## R4 — Session Management

After successful login, the application stores the user's ID in the session.

The user's ID is taken from the authenticated session instead of being trusted from user input.

Users can also log out, which clears the session.

---

## R5 — Display User's To-Do List

After logging in, users can view their own to-do items.

The application retrieves todos using the authenticated user's ID.

Users cannot see another user's todos.

---

## R6 — Add a To-Do

Users can add a new to-do item.

The application validates that the title is not empty and does not exceed the allowed length.

The new todo is associated with the currently logged-in user.

---

## R7 — Edit a To-Do

Users can edit the title and completion status of their own todos.

The update query checks both:

```sql
todo_id
```

and

```sql
user_id
```

to ensure that a user can only modify their own todo.

---

## R8 — Mark a To-Do as Done

Users can mark their todos as completed.

The completion state is stored in the database using the `is_done` field.

---

## R9 — Delete a To-Do

Users can delete their own todos.

The deletion operation also checks the authenticated user's ID so that users cannot delete another user's todo.

---

## R10 — Security and Validation

The application uses several security measures:

* Password hashing with bcrypt
* Parameterized SQL queries
* Session-based authentication
* User ownership checks
* Environment variables for sensitive configuration
* `.env` excluded from Git
* Server-side validation

---

# 6. Screenshots

The required screenshots are stored inside the `screenshots/` folder.

## Registration Page with Error Message

This screenshot demonstrates the registration page and its validation/error messages.

![Register Page Error](screenshots/register%20page%20error.png)

---

## Login Page

This screenshot shows the login page.

![Login Page](screenshots/login%20page.png)

---

## To-Do List with a Completed To-Do

This screenshot shows the to-do list with one task marked as completed.

![Completed To-Do](screenshots/one%20marked%20as%20done.png)

---

## Phone-Sized View

This screenshot demonstrates the application displayed in a phone-sized window.

![Phone Screenshot](screenshots/phone%20screenshot.png)

---

# 7. Database Design

The application uses two main tables:

### Users

The `users` table stores:

* `user_id`
* `email`
* `name`
* `password_hash`
* `registration_date`

The email field is unique, preventing multiple accounts from using the same email.

### Todos

The `todos` table stores:

* `todo_id`
* `user_id`
* `title`
* `is_done`
* `created_at`

The `user_id` field creates a relationship between each todo and its owner.

---

# 8. Required Questions

## (a) Why do UPDATE and DELETE contain `AND user_id = ?`?

The condition:

```sql
AND user_id = ?
```

ensures that a user can only update or delete a todo that belongs to that user.

The application gets the authenticated user's ID from the session.

Without this condition, knowing or guessing another user's `todo_id` could allow a user to modify or delete someone else's todo.

Therefore, the ownership check is an important security measure.

---

## (b) What happens if we insert a todo for a nonexistent `user_id`?

The database rejects the insertion because `todos.user_id` is a foreign key referencing `users.user_id`.

A todo must belong to an existing user.

This demonstrates the database constraint discussed in the lecture:

**Foreign Key Constraint / Referential Integrity**

---

## (c) Why do we store a password hash instead of the actual password?

Passwords should never be stored as plain text.

Instead, the application hashes the password using bcrypt and stores the resulting hash.

During login, the entered password is checked against the stored hash.

This protects users' passwords even if the database is exposed.

---

## (d) If `name` is already `NOT NULL`, why do we still check if the name is empty?

`NOT NULL` only prevents the database value from being `NULL`.

An empty string such as:

```text
""
```

is not `NULL`.

Therefore, the application must perform its own validation to make sure the user actually entered a name.

Application-level validation provides a better user experience and prevents meaningless empty values from being submitted.

---

# 9. SQL Query and Security Considerations

The application uses parameterized SQL queries rather than directly inserting user input into SQL statements.

For example:

```python
cursor.execute(
    "SELECT user_id, name, password_hash FROM users WHERE email = %s;",
    (email,)
)
```

This helps protect the application against SQL injection.

The application also uses the authenticated user's ID from the session when accessing todos.

---

# 10. User Ownership

Each todo belongs to a specific user through:

```text
todos.user_id → users.user_id
```

When retrieving todos, the application uses the logged-in user's ID.

When updating or deleting a todo, the query checks both the todo ID and the user ID.

This ensures that users only have access to their own data.

---

# 11. Validation and Testing

The following cases were considered during testing:

### Registration

* Empty name
* Empty email
* Empty password
* Empty confirmation password
* Password mismatch
* Duplicate email
* Successful registration

### Login

* Empty email
* Empty password
* Unknown email
* Incorrect password
* Correct credentials
* SQL injection attempt

### To-Do Management

* Add a todo
* Edit a todo
* Mark a todo as done
* Delete a todo
* Verify that users only see their own todos

---

# 12. Environment Variables

The application uses environment variables for configuration.

The repository contains:

```text
.env.example
```

The actual `.env` file is excluded through `.gitignore`.

This prevents database credentials and other sensitive configuration from being uploaded to GitHub.

---

# 13. Bonus Features

No bonus feature is claimed for this submission.

---

# 14. Conclusion

This project implements the required Login & To-Do Application using Flask, MySQL, HTML/CSS, and secure authentication practices.

It covers user registration, login, session management, todo creation and management, validation, database relationships, and user-level data ownership.
