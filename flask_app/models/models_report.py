from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.models_user import User

db = 'salesorder_inventory_schema'

class Report:
    def __init__( self , data ):
        self.id = data['id']
        self.total_amount = data['total_amount']
        self.name = data['name']
        self.reorder_level = data['reorder_level']
        self.stock_on_hand = data['stock_on_hand']
        self.whs_name = data['whs_name']
        self.creator = None

    @classmethod
    def get_sales_report(cls):
        query = """
            SELECT u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            sum(h.total_amount) as total_amount,
            NULL as item_name,
            NULL as reorder_level,
            NULL as stock_on_hand,
            NULL as whs_name,
            NULL as name
            FROM users u
            LEFT JOIN order_hdr h
            ON u.id = h.user_id
            LEFT JOIN order_dtl d
            ON h.id = d.id
            GROUP BY u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.password;
            """
        results = connectToMySQL(db).query_db(query)
        daily_sales = []
        for row in results:
            one_sales = cls(row)
            salesman = {
                "id": row['id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": None,
                "password": None,
                "created_at": None,
                "updated_at": None
                }
            creator = User(salesman)
            one_sales.creator = creator
            daily_sales.append(one_sales)

        return daily_sales

    @classmethod
    def reorder_items(cls):
        query = """
                SELECT *,
                NULL as total_amount
                FROM items i
                JOIN warehouse w
                ON w.item_id = i.id
                JOIN warehouse_maint wm
                ON wm.id = w.whs_maintenance_id
                WHERE w.stock_on_hand <= i.reorder_level
                ORDER BY i.name ASC;
                """
        results = connectToMySQL(db).query_db(query)
        items = []
        for item in results:
            items.append( cls(item) )
        print (items)
        return items
