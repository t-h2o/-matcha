"""Flask, psycopg2, os.environ, contextmanager"""

from os import environ
from sys import stderr
from contextlib import contextmanager
from flask import Flask
from flask import request
from flask import jsonify
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UndefinedTable
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_cors import CORS

def flaskprint(message):
    print(message, file=stderr)

app = Flask(__name__)
CORS(app, origins="http://localhost:4200")


@contextmanager
def get_db_connection():
    """Generator of database connection"""

    conn = connect(environ["DATABASE_URL"])
    try:
        yield conn
    finally:
        conn.close()


@app.route("/create")
def create_table_users():
    """Create the Users's table."""

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(12) UNIQUE NOT NULL,
                firstname VARCHAR NOT NULL,
                lastname VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                password VARCHAR NOT NULL
                );
                """
            )
            conn.commit()

    return jsonify({"success": "Table 'users' created"}), 201


@app.route("/login", methods=["POST"])
def login_user():
    """Check the login"""
    json = request.json

    required_fields = ["username", "password"]
    missing_fields = [
        field for field in required_fields if field not in json or not json[field]
    ]

    if missing_fields:
        return (
            jsonify(
                {
                    "error": f"The following fields are required and cannot be empty: {', '.join(missing_fields)}"
                }
            ),
            400,
        )

    try:
        username = json["username"]
        password = json["password"]
    except KeyError as e:
        return jsonify({"error": f"{e} is required."})

    error = None

    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."

    if error is not None:
        return jsonify({"error": error})

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user_db = cur.fetchone()

            if user_db is None:
                return jsonify({"error": "Incorrect username"}), 401
            if check_password_hash(user_db[6], password):
                return jsonify({"success": "loged"})
            return jsonify({"error": "Incorrect password"}), 401

    return "login"


@app.route("/register", methods=["POST"])
def register_user():
    """Register a new user.

    Validates that the username is not already taken.
    Hashes the password for security.
    """
    if request.headers.get("Content-Type") != "application/json":
        return jsonify({"error": "Content-Type not supported!"}), 415

    json = request.json

    try:
        username = json["username"]
        password = json["password"]
        firstname = json["firstname"]
        lastname = json["lastname"]
        email = json["email"]
    except KeyError as e:
        return jsonify({"error": f"{e} is required."})

    error = None

    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."
    elif not firstname:
        error = "Firstname is required."
    elif not lastname:
        error = "Lastname is required."
    elif not email:
        error = "Email is required."

    if error is not None:
        return jsonify({"error": error})

    with get_db_connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password, firstname, lastname, email) VALUES (%s,%s,%s,%s,%s);",
                    (
                        username,
                        generate_password_hash(password),
                        firstname,
                        lastname,
                        email,
                    ),
                )
                conn.commit()
        except conn.IntegrityError:
            return jsonify({"error": f"User {username} is already registered."})

    return jsonify({"succefull": f"User {username} was succefull added"})


@app.route("/drop", methods=["POST"])
def drop_table():
    """Drop table name in JSON"""

    if request.headers.get("Content-Type") != "application/json":
        return jsonify({"error": "Content-Type not supported!"}), 415
    json = request.json
    table = json["table"]

    error = None

    if not table:
        error = "table is required."

    if error is not None:
        return jsonify({"error": error})

    with get_db_connection() as conn:
        try:
            cur = conn.cursor()
            cur.execute(f"DROP table IF EXISTS {table}")
            conn.commit()
            return jsonify({"success": f"Table {table} was successfully dropped"})
        except UndefinedTable:
            return jsonify({"error": "Undefined table"}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
