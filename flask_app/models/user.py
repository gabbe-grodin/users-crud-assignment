import pprint
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

    # ! DELETE
    @classmethod
    def delete_one_user(cls, id):
        query = """
                DELETE FROM users
                WHERE id = %(id)s
                """
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)
