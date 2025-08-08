from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = 'salesorder_inventory_schema'

class Order_By_Group:
    def __init__( self , data ):
        self.description = data['description']
        self.order_hdr_id = data['order_hdr_id']
        self.quantity = data['quantity']
