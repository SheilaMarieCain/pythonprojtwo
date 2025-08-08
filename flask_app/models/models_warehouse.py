from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_inventory import Inventory
from flask_app.models.models_user import User
from flask import flash

db = 'salesorder_inventory_schema'

class Warehouse:
    def __init__( self , data ):
        self.id = data['id']
        self.whs_name = data['whs_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def insert_whs(cls, data ):
        query = """
            INSERT
            INTO warehouse_maint (whs_name)
            VALUES ( %(whs_name)s);
            """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def insert_stock_in(cls, data ):
        query = """
            INSERT
            INTO stock_in ( item_id, quantity)
            VALUES ( %(item_id)s , %(quantity)s);
            """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def update_inventory(cls,data):
        query = """
                SELECT *
                FROM warehouse
                WHERE item_id = %(item_id)s
                AND whs_maintenance_id = %(whs_id)s;
                """
        results = connectToMySQL(db).query_db(query, data)
        if len(results) != 0:
            query = """
                UPDATE warehouse
                SET stock_on_hand=stock_on_hand + %(quantity)s
                WHERE item_id = %(item_id)s
                AND whs_maintenance_id = %(whs_id)s;
                """
            return connectToMySQL(db).query_db(query,data)
        else:
            query = """
                INSERT INTO warehouse (item_id, stock_on_hand, whs_maintenance_id)
                VALUES ( %(item_id)s,  %(quantity)s, %(whs_id)s);
                """
            return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all_whs_dropdown(cls):
        query = """
                SELECT *
                FROM warehouse_maint
                ORDER BY whs_name ASC;
                """
        results = connectToMySQL(db).query_db(query)
        whs = []
        for w in results:
            whs.append( cls(w) )
        print (whs)
        return whs

    @staticmethod
    def validate_warehouse(whs):
        is_valid = True
        if len(whs['whs_name']) == 0:
            flash('Name cannot be blank.', 'warehouse')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_stockin(whs):
        is_valid = True
        if len(whs['quantity']) == 0:
            flash('Quantity cannot be blank.', 'stockin')
            is_valid = False
        return is_valid
