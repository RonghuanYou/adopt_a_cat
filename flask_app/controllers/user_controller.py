from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.cat import Cat
from flask_app.models.application import Application

bcrypt = Bcrypt(app)



@app.route("/")
def home():
    if "uuid" not in session:
        session['uuid'] = None
    return render_template("users/dashboard.html", all_cats=Cat.get_all(), user=User.get_one({"id": session['uuid']}))


# display login and registration form for user account
@app.route("/users/")
def users_index():
    if "uuid" in session and session['uuid'] != None:
        return redirect("/users/dashboard")
    return render_template("users/index.html")


# display all users info, and current user's info
@app.route("/users/dashboard")
def user_dashboard():
    if "uuid" not in session:
        flash("Please log in first")
        return redirect('/users')
    return render_template(
        "users/dashboard.html", 
        all_cats=Cat.get_all(), 
        user=User.get_one({"id": session['uuid']})
    )


# display form to create application
@app.route("/users/application/<int:cat_id>")
def display_application(cat_id):
    if session['uuid'] is None:
        flash("Only registered user can adopt cats")
        return redirect('/')
        
    return render_template(
        "users/application.html", 
        all_cats=Cat.get_all(), 
        cat_id = cat_id,
        user=User.get_one({"id": session['uuid']})
    )


# perform the action of creating application
@app.route("/users/application/create/<int:cat_id>", methods=['POST'])
def create_application(cat_id):
    # validation check for input applicaitons info
    # print("cat_id: ", cat_id)
    data = {
        **request.form,
        "cat_id": cat_id,
        "user_account_id": session['uuid']
    }
    # print("data:", data)
    # print("requst form: ", request.form)
    
    if not Application.application_validate(data):
        return redirect(f"/users/application/{cat_id}")

    # insert values into db
    Application.create(data)
    return redirect("/users/dashboard")


# display page to search more cat's info, user logins, pass id
@app.route("/users/cats_info")
def cats_info():
    if session['uuid']:
        return render_template("users/cats_info.html", user=User.get_one({"id": session['uuid']}))
    else:
        return render_template("users/cats_info.html")


# performing the action of registering an account, before it, check if its valid
@app.route("/users/register", methods=['POST'])
def user_register():
    # check if inputs are valid
    if not User.register_validate(request.form):
        return redirect("/admins")

    # if inputs are valid, hash password and extract data
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password": hashed_password
    }
    # when we register successfully, browser should have sessions
    user_id = User.create(data)
    session['uuid'] = user_id
    return redirect("/users/dashboard")


# performing the action of logining an account
@app.route("/users/login", methods=['POST'])
def user_login():
    # if login info is not valid, redirect to home page
    if not User.login_validate(request.form):
        return redirect("/users")

    # track users login in using session
    user = User.get_by_email({"email": request.form['email']})
    session['uuid'] = user.id
    return redirect("/users/dashboard")


# clear all data in one user
@app.route("/users/logout")
def user_logout():
    session.clear()
    return redirect("/")
