"""
Name: Ikumoluyi  Oluwadamilare

Course: Sdev 300

Instructor: johnson kyle

Project: Lab  #7

Date: May 04 2021


This program uses the flask web framework to develop a web page.
To get this program working, I must import flask and render template
from the flask library, so I can use them to run each html template created.
In this program I created three individual routes which are linked to the
main html file, and I use render template to call each html file.
In the (.PY) path I added two folder named static and template;
the template folder consists of html files while the static contains
the CSS file and background image. I also imported the date & time from
date time, so I could add the date function to my web page. Lastly,
the script.py file contains all the main python code. """

from datetime import datetime
from string import punctuation
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField,  PasswordField, validators
from passlib.hash import sha256_crypt


DTA = 'dta.txt'

app = Flask(__name__)

app.secret_key = " enter your secret key here"


def validate_password(password):
    """validate the password to ensure they met the requirement"""
    if len(password) >= 12:
        if any(c.isupper() for c in password):
            if any(c.islower() for c in password):
                if any(c.isdigit() for c in password):
                    if any(c in punctuation for c in password):
                        return True
    return False


def already_r(username):
    """check for already registered username"""
    with open(DTA, "r") as dta:
        for record in dta:
            d_username, d_password = record.split()
            d_password = d_password + "nothing"
            if d_username == username:
                return True
    return False


class RegisterForm(Form):  # pylint: disable=R0903
    """validate and create form"""
    username = StringField('Username', [validators.length(min=4, max=25)])
    password = PasswordField('Enter password')
    confirm = PasswordField('Confirm Password', [validators.DataRequired(),
                                                 validators.EqualTo('password',
                                                                    message=
                                                                    'Passwords '
                                                                    'do not '
                                                                    'match')])


@app.route("/login", methods=['GET', 'POST'])
def login():
    """takes in user info and check if it matches info in storage"""
    now = datetime.now()
    time = now.strftime('%H:%M:%S')
    date = now.strftime('%Y-%m-%d')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        isvalid = False
        p_valid = False

        # check if username and password already exist
        with open('dta.txt', "r") as dta:
            for record in dta:
                d_username, d_password = record.split()
                if d_username == username:
                    isvalid = True
                    if sha256_crypt.verify(password, d_password):
                        p_valid = True
                        break
                isvalid, p_valid = False, False
        if not isvalid or not p_valid:
            flash("invalid username or password: check your input ")
        else:
            session["username"] = username
            return redirect(url_for("dogbreed"))
    else:
        if "username" in session:
            return redirect(url_for("dogbreed"))

    return render_template("login.html", time=time, date=date)


@app.route('/dogbreed')
def dogbreed():
    """this call in the template (dog breed) and pass in title, description
    time & date"""
    now = datetime.now()
    time = now.strftime('%H:%M:%S')
    date = now.strftime('%Y-%m-%d')
    return render_template("dogbreed.html",
                   title="Five Best Animal Breed type",
                   description ="In this App we would list 5 best breed in dog, "
                                "cat and bird category",
                           time=time, date=date)


@app.route('/catbreed')
def catbreed():
    """ this call in the template (cat breed)"""
    return render_template("catbreed.html")


@app.route('/birdbreed')
def birdbreed():
    """ this call in the template bird breed)"""
    return render_template("birdbreed.html")


@app.route('/table')
def table():
    """ this call in the template table breed)"""
    return render_template("table.html")


@app.route("/", methods=['GET', 'POST'])
def register():
    """handles register: uses the form validate """
    username = None
    password = None
    error = None
    now = datetime.now()
    time = now.strftime('%H:%M:%S')
    date = now.strftime('%Y-%m-%d')
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form["username"]
        password = request.form["password"]

        if not username:
            error = 'Please enter your Username.'
        elif not password:
            error = 'Please enter your Password.'
        elif already_r(username):
            error = 'You are already registered'
        elif not validate_password(password):
            error = 'Make your password more complex'

        if error:
            flash(error)
        else:
            hashed_password = sha256_crypt.hash(password)
            with open("dta.txt", "a") as dta:
                dta.write(username + " " + hashed_password + "\n")
                flash("Registration Successful; Now you can log in. ")
                return redirect(url_for("login"))

    return render_template("register.html", form=form, time=time, date=date)


@app.route('/logout')
def logout():
    """handle logout and display log out message"""
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.2", port=8014)
