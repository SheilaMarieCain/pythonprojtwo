from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import session
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

db = 'salesorder_inventory_schema'

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def insert_user(cls, data ):
        query = """
            INSERT
            INTO users( first_name , last_name, email, password )
            VALUES ( %(first_name)s , %(last_name)s, %(email)s, %(pw_hash)s );
            """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def get_user_details_by_email(cls, data):
        query = """
            SELECT * FROM users
            where email = %(email)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        return results[0]

    @classmethod
    def get_user_details_by_id(cls, data):
        query = """
            SELECT * FROM users
            where id = %(user_id)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        return results[0]

    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First Name must be atleast 2 characters.', 'register')
            is_valid = False
        elif not NAME_REGEX.match(user['first_name']):
            flash("Only letters are allowed in First Name.", 'register')
            isValid = False

        if len(user['last_name']) < 2:
            flash('Last Name must be atleast 2 characters.', 'register')
            is_valid = False
        elif not NAME_REGEX.match(user['last_name']):
            flash("Only letters are allowed in Last Name.", 'register')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address.', 'register')
            is_valid = False

        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL(db).query_db(query, user)
        if len(results) != 0:
            flash('Email ' +  user['email'] + ' already exists.', 'register')
            is_valid = False

        if len(user['password']) < 8:
            flash('Password must be atleast 8 characters.', 'register')
            is_valid = False

        if len(user['confirm_password']) < 8:
            flash('Confirm Password must be atleast 8 characters.', 'register')
            is_valid = False
        elif user['password'] != user['confirm_password']:
            flash("Password and Confirm Password don't match", 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True

        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address.', 'login')
            is_valid = False

        if len(user['password']) < 8:
            flash('Password must be atleast 8 characters.', 'login')
            is_valid = False

        if is_valid:
            query = "SELECT * FROM users where email = %(email)s;"
            results = connectToMySQL(db).query_db(query, user)
            if len(results) != 0:
                if not bcrypt.check_password_hash(results[0]['password'], user['password']):
                    flash('Password is incorrect', 'login')
                    is_valid = False
            else:
                flash('Email does not exists.', 'login')
                is_valid = False
        return is_valid
