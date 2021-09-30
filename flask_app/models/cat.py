from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Cat:
    schema = "adopt_a_cat"

    def __init__(self, data):
        self.id = data['id']
        self.admin_account_id = data['admin_account_id']
        self.name = data['name']
        self.age = data['age']
        self.breed = data['breed']
        self.img_url = data['img_url']
        self.is_adopted = data['is_adopted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO cats(admin_account_id, name, age, breed, img_url, is_adopted)
            VALUES (%(admin_account_id)s, %(name)s, %(age)s, %(breed)s, %(img_url)s, %(is_adopted)s);
        """
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cats;"
        results = connectToMySQL(cls.schema).query_db(query)
        all_cats = []
        for row in results:
            all_cats.append(cls(row))
        return all_cats


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM cats WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        return cls(results[0])


    @classmethod
    def update(cls, data):
        query = """
            UPDATE cats SET name = %(name)s, age = %(age)s, breed = %(breed)s,
            img_url = %(img_url)s, is_adopted = %(is_adopted)s WHERE id = %(id)s;
        """
        return connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM cats WHERE id = %(id)s;"
        return connectToMySQL(cls.schema).query_db(query, data)
