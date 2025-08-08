from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.models_order_by_group import Order_By_Group

db = 'salesorder_inventory_schema'

class Report_Order:
    def __init__( self , data ):
        self.id = data['id']
        self.order_detail = None

    @classmethod
    def get_orders_by_item(cls):
        query = """
            SELECT i.id,
            i.description,
            d.order_hdr_id,
            d.quantity
            FROM items i
            JOIN items_has_order_dtl h
            ON i.id = h.items_id
            JOIN order_dtl d
            ON h.order_dtl_id = d.id
            ORDER BY i.name ASC;
            """
        results = connectToMySQL(db).query_db(query)
        orders = []
        for row in results:
            one_order = cls(row)
            order_det = {
                "description": row['description'],
                "order_hdr_id": row['order_hdr_id'],
                "quantity": row['quantity']
                }
            order_detail = Order_By_Group(order_det)
            one_order.order_detail = order_detail
            orders.append(one_order)

        return orders

    @classmethod
    def get_items_by_order(cls):
        query = """
            SELECT d.order_hdr_id as id,
            i.description,
            d.order_hdr_id,
            d.quantity
            FROM order_dtl d
            JOIN items_has_order_dtl h
            ON d.id = h.order_dtl_id
            JOIN items i
            ON h.items_id = i.id
            ORDER BY d.order_hdr_id ASC, i.name ASC;
            """
        results = connectToMySQL(db).query_db(query)
        items = []
        for row in results:
            one_item = cls(row)
            item_det = {
                "description": row['description'],
                "order_hdr_id": row['order_hdr_id'],
                "quantity": row['quantity']
                }
            item_detail = Order_By_Group(item_det)
            one_item.order_detail = item_detail
            items.append(one_item)

        return items
