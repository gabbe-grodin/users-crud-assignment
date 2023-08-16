import pprint
import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class User:
    DB = 'users_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # ! CREATE
    @classmethod
    def create_user(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email)
                VALUES (%(first_name)s, %(last_name)s, %(email)s)
                """
        result = connectToMySQL(cls.DB).query_db(query, data)
        pprint.pp(result)
        return result
    
    # ! READ
    @classmethod
    def get_all_users(cls):
        query = """
                SELECT * 
                FROM users
                """
        result = connectToMySQL(cls.DB).query_db(query)
        pprint.pp(result)
        users = []
        for user in result:
            users.append(cls(user))
        return users
    
    # ! UPDATE
    @classmethod
    def update_user_by_id(cls, data):
        query = """
                UPDATE users
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW()
                WHERE id = %(id)s;
                """
        result = connectToMySQL(cls.DB).query_db(query, data)
        pprint.pp(result)
        return result

    # ! ALSO UPDATE... OR READ? JON SAID UPDATE IN THE VID
    @classmethod
    def get_one_user_by_id(cls, data):
        query = """
                SELECT *
                FROM users
                WHERE id = %(id)s
                """
        result = connectToMySQL(cls.DB).query_db(query, data)
        pprint.pp(result)
        if result:
            user = cls(result[0])
            return user
        else:
            print("Can't get user.")

    @classmethod
    def get_user_by_email(cls, email):
        query = """
                SELECT *
                FROM users
                WHERE email = %(email)s
                """
        data = {"email": email}
        result = connectToMySQL(cls.DB).query_db(query, data)
        pprint.pp(result)
        if result: # if email (result) exists
            user = cls(result[0]) # instantiate and return user
            return user
        else:
            print("Can't get user.")
            return False

    # ! DELETE
    @classmethod
    def delete_one_user(cls, id):
        query = """
                DELETE FROM users
                WHERE id = %(id)s
                """
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)

    # ! VALIDATION
    @staticmethod
    def validate_user(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(user['first_name']) > 0 and len(user['first_name']) <= 2:
            flash("First name must be at least 2 characters. ")
            is_valid = False
        if len(user['first_name']) <= 0:
            flash("Cannot leave first name field blank. ")
            is_valid = False
        if len(user['last_name']) > 0 and len(user['last_name']) <= 2:
            flash("Last name must be at least 2 characters. ")
            is_valid = False
        if len(user['last_name']) <= 0:
            flash("Cannot leave last name field blank.")
        if len(user['email']) == 0:
            flash("Cannot leave email field blank.")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Email must be in proper format.")
            is_valid = False
        # Don't forget to check if the email address already exists in this database. Can only do this, if there is a get_user_by_email method in model
        if User.get_user_by_email(user['email']):
            flash("Email is already in our system, please try again.")
            is_valid = False
        