from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class Admin:
    schema = "adopt_a_cat"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO admin_accounts(first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM admin_accounts;"
        results = connectToMySQL(cls.schema).query_db(query)

        all_admins = []
        for row in results:
            all_admins.append(cls(row))
        return all_admins


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM admin_accounts WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM admin_accounts WHERE email = %(email)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    #check if the photo name is valid, return boolean
    @staticmethod
    def allowed_files(filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    @staticmethod
    def register_validate(post_data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        # attributes: first_name, last_name, email, password, comfirm_password
        if len(post_data['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(post_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False

        # check email format
        # check if email already exists in db
        if not EMAIL_REGEX.match(post_data['email']):
            flash("Email is not valid!")
            is_valid = False
        elif Admin.get_by_email({"email": post_data['email']}):
            flash("Email is already in use")
            is_valid = False
        elif post_data['email'] != "ronghuan@gmail.com":
            flash("No Authorization to register")
            is_valid = False

        # check length of characters
        # check if passwords match
        if len(post_data['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        elif post_data['password'] != post_data['confirm_password']:
            flash("Two passwords don't match!")
            is_valid = False
        return is_valid


    @staticmethod
    def login_validate(post_data):
        # if email doesn't exist in db, it's invalid
        # if input password doesn't match pass in db, it's invalid
        # user: object type
        admin = Admin.get_by_email({"email": post_data['email']})
        if post_data['email'] != "ronghuan@gmail.com":
            flash("Invalid account")
            return False

        #  post_data['password'] will be hashed automatically
        if not bcrypt.check_password_hash(admin.password, post_data['password']):
            flash("Invalid password")
            return False
        return True


    # when admins create new cat, check if info of cats is valid
    @staticmethod
    def cat_validate(post_data):
        is_valid = True

        # attributes: cat name, age, breed, image, adoption status
        if len(post_data['name']) < 3:
            flash("Cat name must be at least 3 characters.")
            is_valid = False

        if len(post_data['age']) == 0:
            flash("Cat age is required")
            is_valid = False

        if len(post_data['breed']) < 2:
            flash("Cat breed is required")
            is_valid = False
        
        if post_data['img_url'] == "":
            flash("Cat image is required")
            is_valid = False   
        
        if (post_data['is_adopted'] != "No"):
            flash("Adoption status should be No")
            is_valid = False

        return is_valid
