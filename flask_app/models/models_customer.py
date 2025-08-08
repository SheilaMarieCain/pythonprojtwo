from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = 'salesorder_inventory_schema'

class Customer:
    def __init__( self , data ):
        self.customer_id = data['customer_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.contact_no = data['contact_no']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_customers(cls):
        query = """
            SELECT *,
            id as customer_id
            FROM customers
            ORDER BY last_name ASC, first_name ASC;
            """
        results = connectToMySQL(db).query_db(query)
        all_customers = []
        for row in results:
            one_customer = cls(row)
            all_customers.append(one_customer)
        return all_customers

    @classmethod
    def insert_customer(cls, data ):
        query = """
            INSERT
            INTO customers ( first_name, last_name, contact_no)
            VALUES ( %(first_name)s , %(last_name)s, %(contact_no)s);
            """
        return connectToMySQL(db).query_db( query, data )

    @staticmethod
    def validate_customer(customer):
        is_valid = True
        if len(customer['first_name']) == 0:
            flash('First Name cannot be blank.', 'customer')
            is_valid = False
        if len(customer['last_name']) == 0:
            flash('Last Name cannot be blank.', 'customer')
            is_valid = False
        if len(customer['contact_no']) == 0:
            flash('Contact Number cannot be blank.', 'customer')
            is_valid = False
        return is_valid

