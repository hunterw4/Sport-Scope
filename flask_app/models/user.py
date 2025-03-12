from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, url_for
import re


#---   Class For User   ----------------------------------------------------
class User:
    schema = 'sport_scope'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.favorite_team_id = data['favorite_team_id']
        self.favorite_team_name = data['favorite_team_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



#---   Get All User Data   -------------------------------------------------
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = MySQLConnection(cls.schema).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    


#---   Query Save User   ---------------------------------------------------
    @classmethod
    def save_user(cls, data):
        query = """
            INSERT INTO users (name, email, password, created_at, updated_at)
            VALUES (%(name)s, %(email)s, %(password)s, NOW(), NOW());
        """
        return MySQLConnection(cls.schema).query_db(query, data)
    


#---   Get User ID   -------------------------------------------------------
    @classmethod
    def get_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = MySQLConnection(cls.schema).query_db(query, (user_id))
        
        if not results:
            return None
        
        return cls(results[0])
    


#---   Get NAME BY ID   ----------------------------------------------------
    @classmethod
    def get_name_by_id(cls, data):
        query = "SELECT name FROM users WHERE id = %(id)s;"
        results = MySQLConnection(cls.schema).query_db(query, data)
        
        if not results:
            return None
        
        return results[0]["name"]
    


#---   Get Email Data   ----------------------------------------------------
    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = MySQLConnection(cls.schema).query_db(query, data)
        
        if not results:
            return None
        
        return cls(results[0])
    


#---   Validate Account Creation   -----------------------------------------
    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['name']) < 2:
            flash("Name must be at least 2 characters.", "register_error")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email is required.", "register_error")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register_error")
            is_valid = False
        return is_valid  
    


#---   Validate Login   ----------------------------------------------------
    # @staticmethod
    # def validate_login(user):
    #     is_valid = True
    #     if len(user['email']) < 1 or len(user['password']) < 1:
    #         flash("Email and password are required.", "login_error")
    #         is_valid = False
    #     return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        email = user.get('email', '').strip()
        password = user.get('password', '').strip()

        # Check for empty fields
        if not email:
            flash("Email is required.", "login_error")
            is_valid = False
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.", "login_error")
            is_valid = False

        if not password:
            flash("Password is required.", "login_error")
            is_valid = False

        return is_valid
    
        