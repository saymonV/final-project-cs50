import datetime
import random
import re
import json
import sqlite3

from flask import redirect, render_template, session
from functools import wraps

# Expression for validating email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
# Database connect
db_connect = sqlite3.connect ("data/family.db", check_same_thread = False)

# Wrapper function ensures page is shown only for loged in users
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# E-mail format check 
def email_check(e):
    if (re.fullmatch(regex, e)):
        return True
    else:
        return False

# Custom class  
class Group():
    def __init__(self, grp_name, grp_number, creator, hash):
        # Initializing  attributes
        self.name = grp_name
        self.number = grp_number
        self.hash = hash
        self.creator = creator
        self.chores = []
        self.members = []
        self.admins = []

    # Adds a new chore and updates database    
    def add_chore(self, chore):
        self.chores.append(chore)
        save_group(self)

    # Only loads up a chore
    def load_chore(self, chore):
        self.chores.append(chore)

    # Removes a chore from class and updates database
    def remove_chore(self, id):
        for c in self.chores:
            if str(c["id"]) == id:
                self.chores.remove(c)
                save_group(self)

    # Updates a chore to a completed state and updates info and database
    def complete_chore(self, id, name):
        for c in self.chores:
            if str(c["id"]) == id:
                if not c["completed"]:
                    c["completed"] = True
                    c["time_completed"] = datetime.datetime.now().strftime("%H:%M, %d/%m/%y")
                    c["completed_by"] = name 
                    save_chore(c)       
                    save_group(self)

    # Append a new member and update database               
    def add_member (self, profile): 
        self.members.append(profile)
        save_group(self)

    # Only loading up a member
    def load_member(self, profile):
        self.members.append(profile)

    # Removes a member and updates database
    def remove_member (self, name):
        for m in self.members:
            if m["name"] == name:
                self.members.remove(m)
                save_group(self)   
                delete_member(m)

    # Add school table to a member and group. Updates database
    def add_school(self, name, table):
        for m in self.members:
            if m["name"] == name:
              # Using zip to extract list elements in correct order
              # So it is rendered in correct way on a table
              m["time_table"] = list(zip(*table))
              save_group(self)
              save_member(m)

    # Check if current user is a creator of the group
    def is_creator(self, id):
        if self.creator["id"] == id:
            return True
        else:
            return False
        
    # Adds new admin profile to a group and updates database   
    def add_admin (self, profile):
        self.admins.append(profile)
        save_group(self)

    # Removes admin and updates database
    def remove_admin (self, id):
        for a in self.admins:
            if int(a["id"]) == id:
                self.admins.remove(a)
                save_group(self)

    # Only loads up admins to a Group
    def load_admin (self, profile):
        self.admins.append(profile)

# Return Random integer in a given range
def random_group_number():
    return random.randrange(10000,99999)

# Creates a chore       
def generate_chore(title, desc, user_id):
    # Saves current time in given format
    time = datetime.datetime.now().strftime("%H:%M,%S %d/%m/%y")
    return {
    'id': None,
    'title': title,
    'description': desc,
    'user': user_id,
    'completed_by': "",
    'time_posted' : time,
    'time_completed' : "",
    'completed': False,
    }

# Members profile
def generate_member_profile(name, password, grp_number):
    return {
        'name': name,
        'password': password,
        'grp_number': grp_number,
        'time_table': [[""] * 6] * 7,
    } 

# Returns loaded class Group
def load_group():
    # Check if it's a user or a member 
    if user_check(session["user_id"]):
        # User
        group_id = db_connect.execute(
                "SELECT grp_id FROM users WHERE id=?;",
                [session["user_id"]]
        ).fetchone()[0]

        group = db_connect.execute(
                "SELECT grp_class FROM groups WHERE id=?;",
                [group_id]
        ).fetchone()[0]
    
    else:
        # Member
        group_number = db_connect.execute(
            "SELECT grp_number FROM members WHERE id=?;",
            [session["user_id"][:-1]]
        ).fetchone()[0] 

        group = db_connect.execute(
            "SELECT grp_class FROM groups WHERE grp_number=?;",
            [group_number]
        ).fetchone()[0] 
    
    # Loads JSON from database
    group = json.loads(group)

    # Generate custom class Group      
    new_group = Group(
                group['name'], 
                group['number'], 
                group['creator'],
                group['hash'],
                )
    # If there are any chores loads them up in new group  
    if group["chores"]:
        for c in group["chores"]:
            new_group.load_chore(c)

    # As well for the members
    if group["members"]:
        for m in group["members"]:
            new_group.load_member(m)

    # And admins
    if group["admins"]:
        for a in group["admins"]:
            new_group.load_admin(a)

    # Returns new group with all the data inside
    return new_group

# Updates group database
def save_group(group):
    try:
        db_connect.execute(
            "UPDATE groups SET grp_class=? WHERE grp_number=?;",
            [
                json.dumps(group.__dict__),
                group.number,
            ]
        )
        db_connect.commit()
    except sqlite3.Error as e:
        print("Error in save_group", e)

# Save changes to members database
def save_member(profile):
    try:
        db_connect.execute(
            "UPDATE members SET profile=?"
            "WHERE grp_number=?"
            "AND name=?;",
            [
                json.dumps(profile), 
                profile["grp_number"], 
                profile["name"]
            ]
        )
        db_connect.commit()
    except sqlite3.Error as e:
        print("Error in save_member", e)

# Deletes a member from database
def delete_member(profile):
    try:
        db_connect.execute(
            "DELETE FROM members WHERE name=? AND grp_number=?;",
            [
                profile["name"],
                profile["grp_number"]
            ]
        )
        db_connect.commit()
    except sqlite3.Error as e:
        print("Error in delete_member", e)

# Updates chore in database
def save_chore(chore):
    try:
        db_connect.execute(
            "UPDATE chores SET chore=? WHERE id=?;",
            [
                json.dumps(chore),
                int(chore["id"]),
            ]
        )
        db_connect.commit()
    except sqlite3.Error as e:
        print("Error in save_chore", e)

# Checks ID type users = int, members = str
def user_check(id):
    if type(id) == int:
        return True
    else:
        return False

# Deletes group content from database tables
def delete_group_database(grp_number, id, admins):
    # Delete group members from database
    try:
        db_connect.execute(
        "DELETE FROM members WHERE grp_number=?",
        [
            grp_number
        ]
    )
        db_connect.commit()
    except sqlite3.Error as e:
        print("SQL error deleting members")
    # Delete all group chores
    try:
        db_connect.execute(
        "DELETE FROM chores WHERE grp_number=?",
        [
            grp_number
        ]
    )
        db_connect.commit()
    except sqlite3.Error as e:
        print("SQL error deleting chores")
    # Delete group from database
    try:
        db_connect.execute(
        "DELETE FROM groups WHERE grp_number=?",
        [
            grp_number
        ]
    )
        db_connect.commit()
    except sqlite3.Error as e:
        print("SQL error deleting group")
    # Update creators group id
    try:
        db_connect.execute(
        "UPDATE users SET grp_id=? WHERE id=?",
        [
            None,
            id
        ]
    )
        db_connect.commit()
    except sqlite3.Error as e:
        print("SQL error deleting from user")
    # Update admins group ID 
    for a in admins:
        try:
            db_connect.execute(
                "UPDATE users SET grp_id=? WHERE id=?",
                [
                    None,
                    a["id"]
                ]
            )
            db_connect.commit()
        except sqlite3.Error as e:
            print("SQL error updating admins", e)