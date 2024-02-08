import json
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, email_check, Group, random_group_number, generate_chore, load_group, generate_member_profile, user_check, save_group, delete_group_database

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

# Web application has 2 admin levels
# Users - Adults 
# Members - Kids

# Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    try:
        # Returns True if user is logged in, False if members is logged in
        if user_check(session["user_id"]):
            group_id = db_connect.execute(
                "SELECT grp_id FROM users WHERE id=?;",
                [session["user_id"]]
                ).fetchone()[0]
            if group_id:
                return render_template("index.html", group=True)
            else:
                return render_template("index.html", group=False)
        return render_template("index.html", group=True)
    
    
    except KeyError as k:   
        return render_template("index.html")
    except TypeError as t:
        return render_template("index.html")
            
    
# Login page for Users
@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Check user input 
        if not username:
            flash("Please enter username", "error__flash")
        else:
            
            # Convert username to a valid format
            formated_username = f"{username[0].upper()}{username[1:].lower()}"
            # Selecting users if exists in database
            user = db_cursor.execute(
            "SELECT * FROM users WHERE username=?;",
              [formated_username]
              ).fetchone()  
            # If user exists in database proceed
            if user:
                if not password or not check_password_hash(user[2], password):
                    flash("Invalid password", "error__flash")

                # Log in
                else:
                    session.clear()
                    session["user_id"] = user[0]
                # If users is a part of group takes him to group homepage
                    if user[4]:
                        return redirect("/group_home")
                    else:
                        return redirect("/")
            else:
                flash("Invalid username", "error__flash")
        return redirect ("/login")

# Log in page for Members
@app.route("/login_members", methods=["GET", "POST"])
def members_login():
    if request.method == "GET":
        return render_template("login_members.html")
    else:
        group_number = request.form.get("group-number")
        name = request.form.get("member-name")
        password = request.form.get("password-member")
        if not group_number:
            flash("Enter group number", "error_flash")
        elif not name:
            flash("Enter your name", "error_flash")
        elif not password:
            flash("Enter password", "error_flash")
        else:
            formated_name = f"{name[0].upper()}{name[1:].lower()}"
            member = db_cursor.execute(
                    "SELECT * FROM members WHERE name=?"
                    "AND grp_number = ?;",
                [
                    formated_name,
                    group_number
                ]
                ).fetchone()
            if not member:
                flash("Invalid name or group number")
            elif not check_password_hash(member[2], password):
                flash("Invalid password")
            else:
                # Clear session 
                session.clear()
                # Add letter M to ID for Members
                session["user_id"] = f"{str(member[0])}m"
                return redirect("/group_home")
            
    return redirect("/login_members")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        email = request.form.get("email").lower()
        password = request.form.get("user-password")  
        # Ensures data input from user is valid
        if not username or not username.isalpha() or any(char.isspace() for char in username):
            flash("Invalid username", "error__flash")
        elif len(username) > 16:
            flash("Username too long", "error__flash")
        else:
            # Conver username to a valid format
            formated_username = f"{username[0].upper()}{username[1:].lower()}"                 
            # Check if username is already in database
            if db_connect.execute("SELECT * FROM users WHERE username=?;",
                [
                    formated_username
                ]).fetchone():
                flash("Username taken", "error__flash")
            # Email must be in correct format
            elif not email or not email_check(email):
                flash("Invalid e-mail adress", "error__flash")
            # Check if email is already in database
            elif db_connect.execute("SELECT email FROM users WHERE email=?;",
                                    [
                                       email 
                                    ]).fetchone():
                flash("Email already taken", "error__flash")
            # Password check
            elif not password or len(password) < 8:
                flash("Invalid password - Must be at least 8 characters", "error__flash")

            elif request.form.get("check") != password:
                flash("Passwords do not match!", "error__flash")

            else:
                user = db_cursor.execute(
                        "SELECT * FROM users WHERE username=?;", 
                        [formated_username]
                        ).fetchone()
                # Check if usarname is already in database
                if user:
                    flash("Username taken", "error__flash")

                new_password = generate_password_hash(
                                password, 
                                method="pbkdf2", 
                                salt_length=16)

                db_connect.execute(
                    "INSERT INTO users (username, hash, email)"
                    "VALUES (?, ?, ?);",
                        [
                            formated_username, 
                            new_password, 
                            email
                        ]
                )
                db_connect.commit()

                flash("You successfuly created a new account.", "success__flash")
                return redirect("/login")
        return redirect("/register")

# Creates a new group
@app.route("/create_group", methods=["POST"])
@login_required
def create_group():
    # Storing user input in to a variable -- grp short for group
    grp_name = request.form.get("group-name")
    grp_password = request.form.get("group-password")
    # Ensuring input is valid
    if not grp_name or len(grp_name) < 3 or len(grp_name) > 16:
       flash("Enter a group name 3 to 16 characters long", "error__flash") 
    elif not grp_password or len(grp_password) < 6 or len(grp_password) > 16:
        flash("Invalid password", "error__flash")
    elif request.form.get("group-password-check") != grp_password:
        flash("Passwords do not match!", "error__flash")
    else:
        # Generates unique group number
        grp_number = random_group_number()
        while db_connect.execute(
            "SELECT * FROM groups WHERE grp_number=?", 
                [grp_number]).fetchone():
                print("Number taken")
                grp_number = random_group_number()
        # Fetch a current user
        user = db_connect.execute(
            "SELECT * FROM users WHERE id=?",
            [session["user_id"]]
            ).fetchone()
        # Creator's profile
        creator = {
            'name': user[1],
            'id': user[0],
        }
        
        hash = generate_password_hash(
                grp_password, method="pbkdf2", 
                salt_length=16
                )
        # Create custom class Group
        group = Group(grp_name, grp_number, creator, hash)
        
        # Format Group in to JSON 
        json_grp = json.dumps(group.__dict__)
        
        # Save group in database and returning uniqe ID
        try:
            group_id = db_connect.execute(
                "INSERT INTO groups (grp_number, grp_class, creator_id)"
                "VALUES (?, ?, ?)"
                "RETURNING id;",
                       [
                        grp_number, 
                        json_grp,
                        user[0]
                       ]).fetchone()[0]
            db_connect.commit()
            # Updates user with group ID
            db_connect.execute(
                "UPDATE users SET grp_id=? WHERE id=?;",
                [group_id, session["user_id"]]
                )
            db_connect.commit()
            return redirect("/group_home")
        except sqlite3.Error as e:
            flash("Something went wrong", "error__flash")
    return redirect ("/")

# Join a group as users
@app.route("/join_group", methods=["POST"])
@login_required
def join_group():
    grp_number = request.form.get("join-group-number")
    grp_password = request.form.get("join-group-password")
    group = db_connect.execute(
        "SELECT * FROM groups WHERE grp_number=?;",
        [grp_number]
    ).fetchone()
    # Check if group number is valid
    if not grp_number or not group:
        flash("Invalid group number", "error__flash")
        return redirect ("/")
    # Grab group class
    group_class = group[2]
    # Load group in to an object
    group_class = json.loads(group_class)
    
    # Check for user input
    if not check_password_hash(group_class["hash"], grp_password):
        flash("Invalid group password", "error__flash")
    else:
        if len(group_class["admins"]) >= 10:
            flash("Group is full", "error__flash", "error__flash")
        # Update user with new Group ID
        else:
            try:
                db_connect.execute(
                "UPDATE users SET  grp_id=? WHERE id=?;",
                [
                    group[0],
                    session["user_id"]
                ])
                db_connect.commit()

                # If updated call another function 
                return join_group_save()
            except sqlite3.Error as e:
                print("Error updating user", e) 
    return redirect("/")

# Updates group admin list
@app.route("/join_group_save", methods=["POST"])
@login_required
def join_group_save():
    group = load_group()
    name = db_connect.execute(
        "SELECT username FROM users WHERE id=?;",
        [session["user_id"]]
    ).fetchone()[0]
    profile = {
        'id': session["user_id"],
        'name': name,
    }
    group.add_admin(profile)
    flash("Successfully joined a group", "success__flash")
    return redirect("/")


# Group home page
@app.route("/group_home", methods=["GET", "POST"])
@login_required
def group_home():
    if request.method == "GET":
        # Checking if it's a User or Member
        if user_check(session["user_id"]):
            name = db_connect.execute(
                    "SELECT username FROM users WHERE id=?;",
                    [
                        session["user_id"]
                    ]
                ).fetchone()[0]
        else:
            name = db_connect.execute(
                    "SELECT name FROM members WHERE id=?;",
                    [
                        session["user_id"][:-1]
                    ]).fetchone()[0]    
        return render_template("group_home.html", user=user_check(session["user_id"]), name=name)
    
# Chore list 
@app.route("/chores", methods=["GET", "POST"])
@login_required
def chores():
    group = load_group()
    # Render chore list
    if request.method == "GET":
        chores = group.chores
        # If no chores in group generate example 
        if not chores:
            chores = [generate_chore("Example", "Please feed the  dog, food is in the garage.", None)]
        
        # Sorting the list
        sorted_chores = sorted(chores, key= lambda t: t["time_posted"], reverse=True) 
 
        final_sort = sorted(sorted_chores, key = lambda c: c["time_completed"], reverse=True)
    
        return render_template("chores.html", chores=final_sort, members=group.members, id=user_check(session["user_id"]))

    else:
        # Add new chore
        title = request.form.get("title")
        desc = request.form.get("chore_desc")

        if not title  or not desc:
            flash("All fields are requierd", "error__flash")
        # Chore limit per group
        elif len(group.chores) >= 50:
            flash("Maximum number of chorse per group has been reached", "error__flash") 
        else:
            # Generate a chore
            new_chore = generate_chore(title, desc, session["user_id"])
            # Saves it in database
            chore_id = db_connect.execute(
                "INSERT INTO chores (chore, grp_number)"
                "VALUES (?, ?)"
                "RETURNING id;",
                [
                    json.dumps(new_chore),
                    group.number
                ]
            ).fetchone()[0]
            db_connect.commit()
            # Updating database with new ID
            new_chore['id'] = chore_id
            db_connect.execute(
                "UPDATE chores SET chore =?"
                "WHERE id=?;",
                [
                    json.dumps(new_chore),
                    chore_id
                ]
            )
            db_connect.commit()
            group.add_chore(new_chore) 
            flash("New chore successfully added", "success__flash")
        return redirect("/chores")


# Group panel page
@app.route("/group_panel", methods=["GET", "POST"])
@login_required
def group_panel():
    if request.method == "GET":
        group = load_group()
        # Display current user name and members list
        name = db_connect.execute(
                    "SELECT username FROM users WHERE id=?;",
                    [
                        session["user_id"]
                    ]
                ).fetchone()[0]
        return render_template("group_panel.html", members=group.members, name=name)
    
# Add new member to a Group
@app.route("/add_member", methods=["POST"])
@login_required
def add_member():
    group = load_group()
    name = request.form.get("name")
    password = request.form.get("password")
    # Check input from a user
    if not name or len(name) < 3 or len(name) > 16:
        flash("Name must be 3 to 16 characters", "error__flash")

    elif not password  or len(password) < 6 or len(password) > 16:
        flash("Password must be 6 to 12 characters", "error__flash")
        
    elif len(group.members) > 30:
        flash("Maximum number of members", "error__flash")
        
    else:
        formated_name = f"{name[0].upper()}{name[1:].lower()}"
        # Database check if name is taken inside that group only
        if db_connect.execute(
                "SELECT * FROM members WHERE name=? AND grp_number=?;",
                [
                    formated_name,
                    group.number
                ]
            ).fetchall():
            flash("Name taken", "error__flash")
        else:
            # Saves a member and updates databse 
            hash = generate_password_hash(
                    request.form.get("password"),
                    method="pbkdf2", 
                    salt_length=12
                    )
            profile = generate_member_profile(formated_name, request.form.get("password"), group.number)
            try:
                db_connect.execute(
                    "INSERT INTO members (name, hash, grp_number, profile)"
                    "VALUES (?, ?, ?, ?);",
                    [
                        formated_name,
                        hash,
                        group.number,
                        json.dumps(profile)  
                    ]
                )
                db_connect.commit()    
                group.add_member(profile)
                flash("Successfully added a new member", "success__flash")
            except sqlite3.Error as e:
                flash("Something went wrong", "error__flash")     
    return redirect ("/group_panel")
            

# School page 
@app.route("/school", methods=["GET"])
@login_required
def school():
    group = load_group()
    # Check if group has members
    if not group.members:
        return render_template("school.html")  
    return render_template("school.html", members=group.members)

        
    
# Update school page
@app.route("/update_school", methods=["GET", "POST"])
@login_required
def update_school():
    group = load_group()
    week = {
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
        'Sunday': 7,
    }
    if request.method == "GET":
        # Renderds page for a user 
        if user_check(session["user_id"]):
            return render_template("update_school.html", week=week, members=group.members, id=user_check(session["user_id"]))
        # Renders page for a member
        else:
            name = db_connect.execute(
                "SELECT name FROM members where id=?;",
                [session["user_id"][:-1]]
                ).fetchone()[0]
            return render_template("update_school.html", week=week, name=name)
    else:
        
        member = request.form.get("select-member")
        if member == "None":
            flash("Please select a member", "error__flash")
            return redirect ("/update_school")
        
        table = [] * 6
        # Updates table with input data
        for k in week.items():      
            if not k[0] == "Sunday": 
                subjects = []  
                for i in range(7):      
                    subject = request.form.get(f"input-{k[0]}-{i + 1}") 
                    subjects.append(subject)
                table.append(subjects)
        # Update members table 
        group.add_school(member, table)
        flash("Successfully updated", "success__flash")
        return redirect ("/update_school")

# Sends group members to JavaScript
@app.route("/request_members", methods=["POST"])
@login_required
def send_members():
    group = load_group()
    return json.dumps(group.members)
    
# Delete a member after request
@app.route("/delete_member", methods=["POST"])
@login_required
def delete_member():
    group = load_group()
    name = request.get_json()
    group.remove_member(name)
    return "0"

# Delete admin after request
@app.route("/delete_admin", methods=["POST"])
@login_required
def delete_admin():
    group = load_group()
    print("Incoming...")
    name = request.get_json()
    try:
        for a in group.admins:
            if name == a["name"]:
                group.remove_admin(a["id"])
                db_connect.execute(
                    "UPDATE users SET grp_id=? WHERE id=?;",
                    [
                        None,
                        a["id"]
                    ]     
                )
                db_connect.commit()
    except sqlite3.Error as e:
        print("Error in delete admin", e)
    return "0"

# Delete a chore by ID     
@app.route("/delete_chores", methods=["POST"])
def delete_chores():
    group = load_group()
    print("Incoming... delete chores")
    try: 
        chore_id = request.get_json()
        group.remove_chore(chore_id)
        db_connect.execute(
            "DELETE FROM chores WHERE id=?",
            [
                chore_id
            ])
        
        db_connect.commit()   
        return "0"
    except TypeError as e:
        print("Error in delete_chores", e)

# Checks of chore as completed
@app.route("/complete_chore", methods=["POST"])
def complete_chore():
    group = load_group()
   
    try:
        chore_id = request.get_json()
        member = db_connect.execute(
                    "SELECT name FROM members WHERE id=?;",
                    [
                        session["user_id"][:-1]
                    ]
                    ).fetchone()[0]
        # Update chore in Group
        group.complete_chore(chore_id, member)

        return redirect("/chores")
    except TypeError as e:
        print("Error in complete_chores", e)

# Refresh a page
@app.route("/refresh", methods=["POST"])
def refresh():
    return "", 204

# Settings page
@app.route("/settings", methods=["GET"])
@login_required
def settings():
    group = load_group()
    name = db_connect.execute(
                "SELECT username FROM users WHERE id=?;",
            [
                session["user_id"]
            ]
            ).fetchone()[0]
    # Check if current usert is creator of a group
    if group.is_creator(session["user_id"]):
            return render_template("settings.html",admins=group.admins, gn=group.number, creator=True, name=name)
    else:
        return render_template("settings.html",admins=group.admins, gn=group.number, creator=False, name=name)

# Reset user password in Settings
@app.route("/reset_user_password", methods=["POST"])
@login_required
def reset_user_password():
    password = request.form.get("old-password-reset")
    new_password = request.form.get("new-password-reset")
    check = request.form.get("check-reset")
    user = db_connect.execute(
            "SELECT * FROM users WHERE id=?",
            [
                session["user_id"]
            ]
            ).fetchone()
    # Check user input
    if not check_password_hash(user[2], password):
        flash("Invalid password", "error__flash")
    elif len(new_password) < 8:
        flash("Password must be at least 8 characters", "error__flash")
    elif new_password != check:
        flash("Password doesn't match", "error__flash")
    else:
        # Update database
        db_connect.execute(
            "UPDATE users SET hash=?"
            "WHERE id=?;",
            [
                generate_password_hash(
                    new_password, 
                    method="pbkdf2", 
                    salt_length=16),
                session["user_id"]

            ]
        )
        session.clear()
        flash("You successfully changed your password", "success__flash")
        return redirect("/")
    return redirect("/settings")

# Users that are not creators can leave group
@app.route("/leave_group", methods=["POST"])
@login_required
def leave_group():
    group = load_group()
    user = db_connect.execute(
        "SELECT * FROM users WHERE id=?;",
        [
            session["user_id"]
        ]
    ).fetchone()
    # Check password
    if not check_password_hash(user[2], request.form.get("leave-group-password")):
        flash("Invalid password", "error__flash")
        
    else:      
        try:
            # Update database
            db_connect.execute(
                "UPDATE users SET grp_id=? WHERE id=?;",
                [
                    None,
                    session["user_id"]
                ]
            )
            db_connect.commit()

            group.remove_admin(session["user_id"])  
            return redirect("/")
        except sqlite3.Error as e:
            print("Error updating user in Delete", e)
    return redirect("/settings")

# Reset group password by group creator
@app.route("/reset_group_password", methods=["POST"])
@login_required
def reset_group_password():
    group = load_group()
    password = request.form.get("group-password-new")
    # Check user input
    if not check_password_hash(group.hash, request.form.get("group-password-old")):
        flash("Invalid group password", "error__flash")
    elif not password or len(password) < 8:
        flash("New password must be at least 8 characters long", "error__flash")
    elif password != request.form.get("reset-group-password-check"):
        flash("Passwords must match!", "error__flash") 
    else:
        group.hash = generate_password_hash(password, method="pbkdf2", salt_length=16)
        save_group(group)
        flash("Password changed", "success__flash")
        
    return redirect("/settings")


# Delete a group 
@app.route("/delete_group", methods=["POST"])
@login_required
def delete_group():
    group = load_group()
    grp_number = request.form.get("delete-group-number")
    password = request.form.get("delete-group-password")
    user = db_connect.execute(
        "SELECT * FROM users WHERE id=?;",
        [
            session["user_id"]
        ]
    ).fetchone()  

    if not grp_number or int(grp_number) != group.number:
        flash("Incorrect group number", "error__flash")
    elif not password or not check_password_hash(user[2], password):
        flash("Invalid creator's password", "error__flash")
    else:
        # If all input checks out deletes group data, chores and members.
        delete_group_database(group.number, session["user_id"], group.admins)
        return redirect("/")
    
    return redirect("/settings")

# Delete user account
@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    group = load_group()
    password = request.form.get("delete-account-password")
    check = request.form.get("delete-account-check")
    user = db_connect.execute(
        "SELECT * FROM users WHERE id=?;",
        [
            session["user_id"]
        ]
    ).fetchone()  

    if password != check:
        flash("Delete account: Entry doesn't match", "error__flash")

    elif not check_password_hash(user[2], password):
        flash("Delete account: Invalid password", "error__flash")
    
    else:
        # If user is not creator deletes account
        if not group.is_creator(session["user_id"]):
            try:
                db_connect.execute(
                    "DELETE FROM users WHERE id=?;",
                    [
                        session["user_id"]
                    ]
                )        
                db_connect.commit()
                group.remove_admin(session["user_id"])
            except sqlite3.Error as e:
                flash("Something went wrong", "error__flash")
                return redirect("/settings")
            session.clear()
            flash("Successfully deleted your account", "success__flash")
            return redirect("/")
        else:
            # If user is creator of group deletes a group as well
            try:
                db_connect.execute(
                    "DELETE FROM users WHERE id=?;",
                    [
                        session["user_id"]
                    ]
                )        
                db_connect.commit()
            except sqlite3.Error as e:
                flash("Something went wrong", "error__flash")
                return redirect("/settings")
            delete_group_database(group.number, session["user_id"], group.admins)
            session.clear()
            flash("Successfully deleted your account", "success__flash")
            return redirect("/")
    
    return redirect("/settings")