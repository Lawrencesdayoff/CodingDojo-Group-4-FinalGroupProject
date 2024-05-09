from flask_app import app
from flask_app.config.mysqlconnection import *
from flask import flash, session
import re
from flask_app.controllers import users
from flask_app.models import book
from flask_bcrypt import Bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

class User:
    DB = "booktok" 
    def __init__(self, data):
        self.iduser = data['iduser']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = []
        self.recipes = []



    # Create user Models
    @classmethod
    def create(cls, user_data):
        query = """INSERT INTO user (firstname, lastname, email, password) 
                    VALUES(%(firstname)s, %(lastname)s, %(email)s, %(password)s);"""
        created_user = {
            "firstname": user_data['firstname'],
            "lastname": user_data['lastname'],
            "email": user_data['email'],
            "password": bcrypt.generate_password_hash(user_data['password'])
        }  
        result = connectToMySQL(cls.DB).query_db(query, created_user)
        session['email'] = user_data['email']
        return result



    # Read user Models
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.DB).query_db(query)
        user = []
        for u in results:
            user.append(cls(u))
            print("one time")
        return user
    
    @classmethod
    def get_user(cls, id):
        query = "SELECT * FROM user WHERE id = %(id)s"
        data = {"id": id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        user = []
        for u in results:
            user.append(cls(u))
            print("one time")
        return user[0]
    


    # Update user Models
    @classmethod
    def update(cls, data):
        query = """UPDATE user 
                SET firstname=%(firstname)s,lastname=%(lastname)s,email=%(email)s
                WHERE iduser = %(iduser)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)


    # Delete user Models
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM user WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)

    # Validations
    @classmethod
    def get_by_email(cls,user):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        data = { "email" : user }
        result = connectToMySQL(cls.DB).query_db(query, data)


        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_info(user):
        print("userinfo")
        print( user)
        is_valid = True
        if "email" in user:
            print("registration")
            list_of_emails = User.get_by_email(user['email'])
            if user['firstname'].isalpha() == False:
                flash('Only letters please')
                is_valid = False
            if len(user['firstname'])< 2:
                flash('First name must be more than one character')
                is_valid = False
            if user['lastname'].isalpha() == False:
                flash('Only letters please')
                is_valid = False
            if len(user['lastname'])< 2:
                flash('Last name needs to be more than one character')
                is_valid = False
            if len(user['password']) < 8:
                flash('Please enter a password with at least 8 characters')
                is_valid = False
            if user['confirm_pass'] != user['password']:
                flash('Passwords do not match!')
                is_valid = False
            if not EMAIL_REGEX.match(user['email']):
                flash("Invalid email address!")
                is_valid = False
            if list_of_emails:
                flash("There already exists a user with this email")
                is_valid = False

        if "email_login" in user:
            user_email= User.get_by_email(user['email_login'])
            if len(user["email_login"]) < 3:
                flash("You must put in an email")
                is_valid = False
            if not EMAIL_REGEX.match(user['email_login']):
                flash("Invalid email address!")
                is_valid = False
            if user_email == False:
                flash("Invalid email")
                is_valid = False
            if len(user['password_login']) < 8:
                flash('Please enter a password with at least 8 characters')
                is_valid = False
            if user_email == True:
                if not bcrypt.check_password_hash(user_email.password, user['password_login']):
                    flash("Invalid Email/Password")
                    is_valid = False
                        
        return is_valid
    
    @staticmethod
    def validate_login_info(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email_login']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['password_login']) < 8:
            flash('Please enter a password with at least 8 characters')
            is_valid = False
        return is_valid

