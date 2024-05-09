
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.
from flask_bcrypt import Bcrypt
# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
bcrypt = Bcrypt(app)
class User:
    DB = "booktok" 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = []



    # Create Users Models
    @classmethod
    def save(cls, user_data):
        query = """INSERT INTO users (first_name, last_name, email, password) 
                    VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        created_user = {
            "first_name": user_data['first_name'],
            "last_name": user_data['last_name'],
            "email": user_data['email'],
            "password": bcrypt.generate_password_hash(user_data['password'])
        }  
        result = connectToMySQL(cls.DB).query_db(query, created_user)
        session['email'] = user_data['email']
        return result



    # Read Users Models
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for u in results:
            users.append(cls(u))
            print("one time")
        return users
    
    @classmethod
    def get_user(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {"id": id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        users = []
        for u in results:
            users.append(cls(u))
            print("one time")
        return users[0]
    


    # Update Users Models
    @classmethod
    def update(cls, data):
        query = """UPDATE users 
                SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s
                WHERE iduser = %(iduser)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)


    # Delete Users Models
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM users WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)

    # Validations
    @classmethod
    def get_by_email(cls,user):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = { "email" : user }
        result = connectToMySQL(cls.DB).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate_info(user):
        is_valid = True
        if "email" in user:
            print("registration")
            list_of_emails = User.get_by_email(user['email'])
            if user['first_name'].isalpha() == False:
                flash('Only letters please')
                is_valid = False
            if len(user['first_name'])< 2:
                flash('First name must be more than one character')
                is_valid = False
            if user['last_name'].isalpha() == False:
                flash('Only letters please')
                is_valid = False
            if len(user['last_name'])< 2:
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


