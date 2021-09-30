from flask import render_template, redirect, request, session, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.admin import Admin
from flask_app.models.cat import Cat
from flask_app.models.application import Application

import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/Users/ronghuanyou/desktop/python/adopt_a_cat/flask_app/static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bcrypt = Bcrypt(app)

# display login and registration form for user account
@app.route("/admins/")
def admins_index():
    if "admin_uuid" in session:
        return redirect("/admins/dashboard")
    return render_template("admins/index.html")


# display all users info, and current user's info
@app.route("/admins/dashboard")
def dashboard():
    # if user is not in session, user is not allowed to go to any page if they don't login
    if "admin_uuid" not in session:
        flash("Please log in first")
        return redirect('/admins')
    
    return render_template(
        "admins/dashboard.html", 
        all_cats = Cat.get_all(), 
        admin=Admin.get_one({"id": session['admin_uuid']})
    )

# ============================================
# perform action of creating a new cat
@app.route("/admins/create", methods=['POST'])
def create_cat():
    # check if the post request has the file part
    if 'img_url' not in request.files:
        flash('No file part')
        return redirect(request.url)

    # file dict to get photo url
    file = request.files['img_url']

    data = {
        **request.form,
        "img_url": file.filename,
        "admin_account_id": session['admin_uuid']
    }

    # validation check for input cats' info
    if not Admin.cat_validate(data):
        return redirect("/admins/dashboard")
    

    # if photo extension is right and photo exists, upload it and update the data storing in db
    if file and Admin.allowed_files(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # create cat in db
        Cat.create(data)
        return redirect("/admins/dashboard")
# ============================================


# display all applications applicants submitted
@app.route("/admins/all_applications")
def all_applications():
    return render_template(
        "admins/all_applications.html",
        all_applications = Application.get_all_applications(),
        admin=Admin.get_one({"id": session['admin_uuid']})
    )


# read single cat info
@app.route("/admins/read/<int:cat_id>")
def read_cat(cat_id):
    return render_template(
        "admins/read_cat.html", 
        cat = Cat.get_one({"id": cat_id}),
        admin=Admin.get_one({"id": session['admin_uuid']})
    )


# display form to edit cat info
@app.route("/admins/edit/<int:cat_id>")
def edit_cat(cat_id):
    return render_template(
        "admins/edit_cat.html", 
        cat = Cat.get_one({"id": cat_id}),
        admin=Admin.get_one({"id": session['admin_uuid']})
    )


# perform the action of updating specific cat info
@app.route("/admins/update/<int:cat_id>", methods=['POST'])
def update_cat(cat_id):
    # todo: validation check 
    if 'img_url' not in request.files:
        flash('No file part')
        return redirect(f"/admins/edit/{cat_id}")   

    # file dict to get photo url
    file = request.files['img_url']

    data = {
        **request.form,
        "id": cat_id,
        "img_url": file.filename,
        "admin_account_id": session['admin_uuid']
    }

    # validation check for input cats' info
    if not Admin.cat_validate(data):
        return redirect(f"/admins/edit/{cat_id}")   

    if file and Admin.allowed_files(file.filename):
        print("success")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # create cat in db
        Cat.update(data)
        return redirect("/admins/dashboard")


# delete specific cat info
@app.route("/admins/delete/<int:cat_id>")
def delete_cat(cat_id):
    Cat.delete({"id": cat_id})
    return redirect("/admins/dashboard")    


# performing the action of registering an account, before it, check if its valid
@app.route("/admins/register", methods=['POST'])
def admin_register():
    # check if inputs are valid
    if not Admin.register_validate(request.form):
        return redirect("/admins")

    # if inputs are valid, hash password and extract data
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password": hashed_password
    }
    # when we register successfully, browser should have sessions
    admin_id = Admin.create(data)
    session['admin_uuid'] = admin_id
    return redirect("/admins/dashboard")


# performing the action of logining an account
@app.route("/admins/login", methods=['POST'])
def admin_login():
    # if login info is not valid, redirect to home page
    if not Admin.login_validate(request.form):
        return redirect("/admins")

    # track users login in using session
    admin = Admin.get_by_email({"email": request.form['email']})
    session['admin_uuid'] = admin.id
    return redirect("/admins/dashboard")


# clear all data in one user
@app.route("/admins/logout")
def admin_logout():
    session.clear()
    return redirect("/")


