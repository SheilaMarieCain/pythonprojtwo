from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.models_user import User

db = 'salesorder_inventory_schema'

class Order:
    def __init__( self , data ):
        self.id = data['id']
        self.customer_id = data['customer_id']
        self.user_id = data['user_id']
        self.order_date = data['order_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def insert_order_hdr(cls, data):
        query = """
            INSERT
            INTO order_hdr ( customer_id, total_amount, remarks, user_id, order_date)
            VALUES ( %(customer_id)s, %(amount)s, %(remarks)s, %(user_id)s, %(order_date)s);
            """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def insert_order_dtl(cls, data ):
        query = """
            INSERT
            INTO order_dtl ( order_hdr_id, item_id, quantity, unit_price, amount )
            VALUES ( %(order_hdr_id)s, %(item_id)s, %(quantity)s, %(selling_price)s, %(amount)s);
            """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def insert_items_has_order_dtl(cls, data ):
        query = """
            INSERT
            INTO items_has_order_dtl ( items_id, order_dtl_id)
            VALUES ( %(item_id)s, %(order_dtl_id)s);
            """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def update_inventory(cls, data ):
        query = """
            UPDATE warehouse
            SET stock_on_hand = stock_on_hand - %(quantity)s
            where item_id = %(item_id)s
            and whs_maintenance_id = %(whs_id)s;
            """
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def update_order_hdr(cls, data ):
        query = """
            UPDATE order_hdr
            SET total_amount = total_amount + %(amount)s
            where id = %(order_hdr_id)s;
            """
        return connectToMySQL(db).query_db( query, data )

    @staticmethod
    def validate_order(order):
        is_valid = True
        if len(order['order_date']) == 0:
            flash('Order Date cannot be blank.', 'order')
            is_valid = False
        if len(order['item_id']) == 0:
            flash('Item Name cannot be blank.', 'order')
            is_valid = False
        if len(order['quantity']) == 0:
            flash('Quantity cannot be blank.', 'order')
            is_valid = False
        if len(order['stock_on_hand']) == 0:
            flash('Stock On Hand cannot be blank.', 'order')
            is_valid = False
        else:
            if int(order['quantity']) > int(order['stock_on_hand']):
                flash('Insufficient stocks. Stock On Hand is ' + order['stock_on_hand'], 'order')
                is_valid = False
        return is_valid
