from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_user import User
from flask import flash, session

db = 'salesorder_inventory_schema'

class Inventory:
    def __init__( self , data ):
        self.id = data['id']
        self.item_id = data['item_id']
        self.name = data['name']
        self.description = data['description']
        self.unit_price = data['unit_price']
        self.selling_price = data['selling_price']
        self.reorder_level = data['reorder_level']
        self.stock_on_hand = data['stock_on_hand']
        self.whs_maintenance_id = data['whs_maintenance_id']
        self.user_id = session['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @classmethod
    def insert_item(cls, data ):
        query = """
            INSERT
            INTO items ( name, description, unit_price, selling_price, reorder_level, user_id)
            VALUES ( %(name)s , %(description)s, %(unit_price)s , %(selling_price)s, %(reorder_level)s, %(user_id)s);
            """
        print('insert_item',query)
        return connectToMySQL(db).query_db( query, data )

    @classmethod
    def update_item(cls,data):
        query = """
            UPDATE items
            SET name=%(name)s,
            description=%(description)s,
            unit_price=%(unit_price)s,
            selling_price=%(selling_price)s,
            reorder_level=%(reorder_level)s
            WHERE id = %(id)s;
            """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete_item(cls, data):
        query = """
            DELETE
            FROM items
            where id = %(id)s;
            """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all_items_per_whs(cls, data):
        query = """
            SELECT *
            FROM items i
            JOIN users u
            ON i.user_id = u.id
            LEFT JOIN warehouse w
            ON w.item_id = i.id
            LEFT JOIN warehouse_maint wm
            ON w.whs_maintenance_id = wm.id
            WHERE wm.id = %(whs_id)s
            ORDER BY i.name ASC;
            """
        results = connectToMySQL(db).query_db(query, data)
        all_items = []
        if results != 0:
            for row in results:
                one_item = cls(row)
                one_item_creator = {
                    "id": row['user_id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at']
                }
                creator = User(one_item_creator)
                one_item.creator = creator
                all_items.append(one_item)
        return all_items

    @classmethod
    def get_one_item(cls, data):
        query = """
            SELECT *
            FROM items i
            LEFT JOIN warehouse w
            ON w.item_id = i.id
            where i.id = %(id)s
            AND w.whs_maintenance_id = %(whs_maintenance_id)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def edit_one_item(cls, data):
        query = """
            SELECT *,
            NULL as stock_on_hand,
            NULL as whs_maintenance_id,
            id as item_id
            FROM items
            where id = %(id)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_items_not_in_whs(cls):
        query = """
                SELECT *,
                id as item_id,
                NULL as stock_on_hand,
                NULL as whs_maintenance_id,
                NULL as first_name,
                NULL as last_name,
                NULL as email,
                NULL as password
                FROM items
                WHERE NOT EXISTS(SELECT 1 FROM warehouse WHERE warehouse.item_id = items.id);
                """
        results = connectToMySQL(db).query_db(query)
        all_items = []
        if results != 0:
            for row in results:
                one_item = cls(row)
                one_item_creator = {
                    "id": row['user_id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['created_at'],
                    "updated_at": row['updated_at']
                }
                creator = User(one_item_creator)
                one_item.creator = creator
                all_items.append(one_item)
        return all_items

    @classmethod
    def get_all_items(cls):
        query = """
            SELECT *,
            id as item_id,
            NULL as stock_on_hand,
            NULL as whs_maintenance_id
            FROM items;
            """
        results = connectToMySQL(db).query_db(query)
        all_items = []
        for row in results:
            one_item = cls(row)
            all_items.append(one_item)
        return all_items

    @staticmethod
    def validate_item(item):
        is_valid = True
        if len(item['name']) == 0:
            flash('Name cannot be blank.', 'item')
            is_valid = False
        if len(item['description']) == 0:
            flash('Description cannot be blank.', 'item')
            is_valid = False
        if len(item['unit_price']) == 0:
            flash('Unit Price cannot be blank.', 'item')
            is_valid = False
        if len(item['selling_price']) == 0:
            flash('Selling Price cannot be blank.', 'item')
            is_valid = False
        if len(item['reorder_level']) == 0:
            flash('Reorder Level cannot be blank.', 'item')
            is_valid = False
        return is_valid
