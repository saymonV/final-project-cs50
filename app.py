import datetime
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, email_check

# Aplication configuration
app = Flask (__name__)

# Configure session to use filesystem

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Setting up SQLite database
db_connect = sqlite3.connect ("data/family.db", check_same_thread = False)
db_cursor = db_connect.cursor()
# Ensures responses are not cached
# Taken from finance project
@app.after_request
def after_request(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template("index.html")
    else:
        return


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        db_cursor.execute("SELECT * FROM users WHERE username = ?;", [request.form.get("username")])
        print(db_cursor.fetchone())
        if not request.form.get("username"):
            error = "Enter username"
        elif not request.form.get("password"):
            error = "Enter password"
        elif db_cursor.fetchone() == None:
            error = "Invalid username"
        elif not check_password_hash(db_cursor.fetchone()[2], request.form.get("password")):
            error = "Invalid password"
        
        else:
            return redirect("/")
        return render_template("login.html", error=error)
        

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("username") or not request.form.get("username").isalpha():
            error = "Invalid username"
        elif not request.form.get("password") or len(request.form.get("password")) < 8:
            error = "Invalid password - Must be at least 8 characters"

        elif request.form.get("check") != request.form.get("password"):
            error = "Passwords must match!"
        elif not request.form.get("email") or not email_check(request.form.get("email")):
            error = "Invalid e-mail adress"
        else:
            username = request.form.get("username")
            password = generate_password_hash(
                request.form.get("password"), method="pbkdf2", salt_length=16)
            email = request.form.get("email")
    
            sql = "INSERT INTO users (username, hash, email) VALUES (?, ?, ?)"
            db_connect.execute(sql, [username, password, email])
            db_connect.commit()
            flash("You successfuly created a new account.")
            return redirect("/login")
        return render_template("register.html", error=error)

@app.route("/lost_password", methods=["GET", "POST"])
def reset_password():

    if request.method == "GET":
        return render_template("lost_password.html")
    else:
        return