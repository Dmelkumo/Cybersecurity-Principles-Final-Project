"""
David Melkumov
CS 166
Lab 8

Python flask app, runs the webpage and contains all the routes
that are used in the webpage. Also renders the pages and performs
actions such as logging in or creating a new account.
"""

import os
import sys
from flask import Flask, render_template, request, url_for, redirect, flash, session
from helpers import authenticate, test_password, generate_strong_pass, hash_password, get_from_db, write_to_db
import traceback
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(20)

# Dictionary for access levels (Access Control Matrix)
PERMISSIONS = {"Time Reporting": 1, "Accounting": 2, "IT Helpdesk": 2, "Engineering Documents": 3}


@app.route("/")
def main_page():
    """
    Render home page, initialize some session variables
    """

    # Initialize global variables, make sure to go to this page before login
    if 'login_attempts' not in session:
        session['login_attempts'] = 0

    # Display who is currently logged in
    if "current_user" in session:
        flash("Currently logged in as " + session['current_user'], 'alert-light')

    return render_template("home.html")


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    """
    Attempts to create the account after ensuring it meets
    the requirements and is not a dupe
    """

    # Constant for least privileged access level
    DEFAULT_ACCESS_LEVEL = 1

    # Display who is currently logged in
    if "current_user" in session:
        flash("Currently logged in as " + session['current_user'], 'alert-light')

    # Get info from form
    if request.method == 'POST':
        form_username = request.form.get('username')
        form_password = request.form.get('password')

        # Get info from database
        row = get_from_db("SELECT * FROM accounts WHERE accounts.username = (?)", [form_username])

        # Ensure that this is not a duplicate username
        if row is not None:
            flash("This account already exists, please try again", 'alert-danger')
            return render_template("create_account.html", value="")

        # Determine if the password meets the requirements
        if not test_password(form_password):
            flash("Your password is not strong enough. Please include uppercase, lowercase, numbers, and special chars, between 8 and 25 characters", 'alert-danger')
            return render_template("create_account.html", value="")

        # Write the account to the database and let the user know
        write_to_db("INSERT INTO accounts VALUES (?, ?, ?)", [form_username, hash_password(form_password), DEFAULT_ACCESS_LEVEL])
        flash("Successfully created account " + form_username + ", log in on the other page", 'alert-success')

    # Render template regardless
    return render_template("create_account.html", value="")


@app.route("/generate_password", methods=['GET', 'POST'])
def generate_password():
    """
    Generates a strong password and inserts it into the password
    input box, as well as displaying it in an alert
    """

    # Generate the password
    password = generate_strong_pass()

    # User feedback/info
    flash("Your password is: " + password, 'alert-info')

    return render_template("create_account.html", value=password)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Attempts to log the user in, redirects to user page if successful
    otherwise stays at login page, max attempts 3
    """

    # Constant for maximum attempts allowed
    MAX_ATTEMPTS = 3

    # In case the user skipped the homepage
    if 'login_attempts' not in session:
        session['login_attempts'] = 0

    # Display who is currently logged in
    if "current_user" in session:
        flash("Currently logged in as " + session['current_user'], 'alert-light')

    # Get info from form
    if request.method == 'POST':
        form_username = request.form.get('username')
        form_password = request.form.get('password')

        # Get info from database
        row = get_from_db("SELECT * FROM accounts WHERE accounts.username = (?)", [form_username])

        # Ensure the row is not empty/username exists
        if row is not None:
            # If the password matches
            if authenticate(row[1], form_password) and int(session['login_attempts']) < MAX_ATTEMPTS:
                # Set the username/current user
                session['current_user'] = form_username
                # Set the access level
                session['current_access_level'] = row[2]
                return redirect(url_for('successful_login'))
        # Increment login attempts
        if 'login_attempts' in session:
            session['login_attempts'] = int(session['login_attempts']) + 1

        # Feedback for user, would have returned already if successful
        if int(session['login_attempts']) >= MAX_ATTEMPTS:
            flash("Too many failed attempts, you can no longer log in", 'alert-warning')
        else:
            flash("Invalid username or password!", 'alert-danger')

    # If it failed to log in or invalid form data
    return render_template("login.html")


@app.route("/successful_login", methods=['GET', 'POST'])
def successful_login():
    """
    Shows the user the successful login page
    with the various buttons representing options
    that they can perform based on their access level
    """

    # Inform the user they are logged in
    if "current_user" in session:
        flash("Currently logged in as " + session['current_user'], 'alert-light')

    # Prevent not logged in users from accessing the page
    if 'current_user' not in session:
        return "<p>Please log in to view this page</p>"

    # If the user is logged in display proper page
    return render_template("successful_login.html")


@app.route("/time_reporting", methods=['GET', 'POST'])
def time_reporting():
    """
    Shows output based on whether or not the user
    had access to this option
    """

    # Simple output based on access level
    if PERMISSIONS["Time Reporting"] <= session["current_access_level"]:
        return "<p>You have accessed Time Reporting</p>"
    else:
        return "<p>You do NOT have access to Time Reporting</p>"


@app.route("/accounting", methods=['GET', 'POST'])
def accounting():
    """
    Shows output based on whether or not the user
    had access to this option
    """

    # Simple output based on access level
    if PERMISSIONS["Accounting"] <= session["current_access_level"]:
        return "<p>You have accessed Accounting</p>"
    else:
        return "<p>You do NOT have access to Accounting</p>"


@app.route("/helpdesk", methods=['GET', 'POST'])
def helpdesk():
    """
    Shows output based on whether or not the user
    had access to this option
    """

    # Simple output based on access level
    if PERMISSIONS["IT Helpdesk"] <= session["current_access_level"]:
        return "<p>You have accessed IT Helpdesk</p>"
    else:
        return "<p>You do NOT have access to IT Helpdesk</p>"


@app.route("/engineering", methods=['GET', 'POST'])
def engineering():
    """
    Shows output based on whether or not the user
    had access to this option
    """

    # Simple output based on access level
    if PERMISSIONS["Engineering Documents"] <= session["current_access_level"]:
        return "<p>You have accessed Engineering Documents</p>"
    else:
        return "<p>You do NOT have access to Engineering Documents</p>"


if __name__ == '__main__':
    try:
        app.run(debug=app.debug, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()
