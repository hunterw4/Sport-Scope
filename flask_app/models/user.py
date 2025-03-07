# User class should go here.
from flask_app.config.mysqlconnection import connect_to_mysql
from flask import flash
import re


email_regex = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z],{2,}$')
passwd_regex = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")   
class users:
  
    db = "sport_scope_schema"
    def __init__(self,data):
        self.first_name =  data['first_name']
        self.last_name =  data['last_name']
        self.email = data['email']
        self.passwd =data['passwd']
        self.created_at =data['created_at']
        self.updated_at = data['updatede_at']
    
    @classmethod
    def get_users(cls):
        query = """SELECT * FROM users;"""
        returnedInfo = connect_to_mysql(cls.db).query_db(query)
        return returnedInfo
    
        
    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users WHERE email= %(email)s;"""
        returnedInfo = connect_to_mysql(cls.db).query_db(query,data)
        return returnedInfo
    
        
    @classmethod
    def add_user(cls,data):
        query = """INSERT INTO users(first_name,last_name,email,passwd,created_at) values(%(first_name)s,%(last_name)s,%(email)s,%(passwd)s,NOW());"""
        returnedInfo = connect_to_mysql(cls.db).query_db(query,data)
        return returnedInfo
    
        
    @classmethod
    def update_user(cls,data):
        query = """UPDATE users SET 'first_name =%(first_name)s,last_name=%(last_name)s,email=%(email)s,updated_at = NOW() WHERE id= %(id)s;"""
        returnedInfo = connect_to_mysql(cls.db).query_db(query,data)
        return returnedInfo
    
    @classmethod
    def update_user_password(cls,data):
        query = """UPDATE users SET 'passwd =%(passwd)s,updated_at = NOW() WHERE email= %(email)s;"""
        returnedInfo = connect_to_mysql(cls.db).query_db(query,data)
        return returnedInfo
    
    @classmethod
    def update_user_email(cls,data):
        query = """UPDATE users SET email=%(email)s,updated_at = NOW() WHERE id= %(id)s;"""
        returnedInfo = connect_to_mysql(cls.db).query_db(query,data)
        return returnedInfo
    
    @staticmethod
    def isValid(data,passwd=None,category=None):
        valid = True
        if len(data['first_name'])<2:
            flash('You First Name must be longer than 2',category)
            valid = False
        if len(data['last_name'])<2:
            flash('You Last Name must be longer than 2',category)
            valid = False
        if email_regex(data['email']) == False:
            flash('Enter a valid Email',category)
            valid = False
            
        if passwd_regex(passwd) == False:
            flash('Enter a valid password',category)
            valid = False
        return valid