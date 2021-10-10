from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import cat
from flask_app.models import user
from flask import flash

class Application:
    schema = "adopt_a_cat"

    def __init__(self, data):
        self.id = data['id']
        self.user_account_id = data['user_account_id']
        self.cat_id = data['cat_id']
        self.dog_num = data['dog_num']
        self.cat_num = data['cat_num']
        self.child_num = data['child_num']
        self.get_vaccines = data['get_vaccines']
        self.energy_level = data['energy_level']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.user = None
        self.cat = None
        

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO applications(user_account_id, cat_id, dog_num, cat_num, child_num, get_vaccines, energy_level)
            VALUES (%(user_account_id)s, %(cat_id)s, %(dog_num)s, %(cat_num)s, %(child_num)s, %(get_vaccines)s, %(energy_level)s);
        """
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def get_all_applications(cls):
        query = """
            SELECT * FROM applications
            LEFT JOIN user_accounts ON user_accounts.id = applications.user_account_id
            LEFT JOIN cats ON cats.id = applications.cat_id;
        """

        results = connectToMySQL(cls.schema).query_db(query)
        all_applications = []
        if results:
            for i in range(len(results)):
                application = cls(results[i])
                row = results[i]
                row_cat_data = {
                    'id': row['cats.id'], 
                    'admin_account_id': row['admin_account_id'],
                    'name': row['name'],
                    'age': row['age'], 
                    'breed': row['breed'],
                    'img_url': row['img_url'],
                    'is_adopted': row['is_adopted'],
                    'created_at': row['cats.created_at'],
                    'updated_at': row['cats.updated_at'],
                }

                row_users_data = {
                    'id': row['user_accounts.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['user_accounts.created_at'],
                    'updated_at': row['user_accounts.updated_at'],
                }
                application.cat = cat.Cat(row_cat_data)
                application.user = user.User(row_users_data)
                all_applications.append(application)
            return all_applications
        return all_applications

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM applications WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        return cls(results[0])


    # when user submits a new application, check application info is valid or not
    @staticmethod
    def application_validate(post_data):
        is_valid = True

        # attributes: 
        if len(post_data['dog_num']) == 0:
            flash("Dog number is required")
            is_valid = False

        if len(post_data['cat_num']) == 0:
            flash("Cat number is required")
            is_valid = False

        if len(post_data['child_num']) == 0:
            flash("Child number is required")
            is_valid = False
        
        if post_data['get_vaccines'] == "":
            flash("Vaccine info is required")
            is_valid = False   
        
        if post_data['energy_level'] == "":
            flash("Energy expectation is required")
            is_valid = False

        return is_valid
