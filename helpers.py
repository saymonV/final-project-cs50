import csv
import datetime
import subprocess
import urllib
import uuid
import re

from flask import redirect, render_template, session
from functools import wraps
# Expression for validating email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# Ensures page is shown only for loged in users
# Code taken from finance project
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def email_check(e):
    if (re.fullmatch(regex, e)):
        return True
    else:
        return False
