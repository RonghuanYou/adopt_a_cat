from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
# from flask_app.models.recipe import Recipe

bcrypt = Bcrypt(app)

# display login and registration form
@app.route("/")
def index():
    if "uuid" in session:
        return redirect("users/dashboard")
    return render_template("users/index.html")


# display all users info, and current user's info
# @app.route("/dashboard")
# def dashboard():
#     # if user is not in session, user is not allowed to go to any page if they don't login
#     if "uuid" not in session:
#         flash("Please log in first")
#         return redirect('/')

#     return render_template(
#         "users/dashboard.html", 
#         all_recipes = Recipe.get_all(), 
#         logged_in_user = User.get_one({"id": session['uuid']})
#     )





















# performing the action of registering an account, before it, check if its valid
@app.route("/register", methods=['POST'])
def register():
    # check if inputs are valid
    if not User.register_validate(request.form):
        return redirect("/")

    # if inputs are valid, hash password and extract data
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password": hashed_password
    }
    # when we register successfully, browser should have sessions
    user_id = User.create(data)
    session['uuid'] = user_id
    return redirect("/dashboard")


# performing the action of logining an account
@app.route("/login", methods=['POST'])
def login():
    # if login info is not valid, redirect to home page
    if not User.login_validate(request.form):
        return redirect("/")

    # track users login in using session
    user = User.get_by_email({"email": request.form['email']})
    session['uuid'] = user.id
    return redirect("/dashboard")


# clear all data in one user
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
