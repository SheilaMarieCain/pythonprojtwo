from flask_app import app
from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.models_inventory import Inventory
from flask_app.models.models_warehouse import Warehouse
from flask_app.models.models_user import User
from flask import flash

@app.route("/new_warehouse")
def new_warehouse():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id']
        }
    return render_template("new_warehouse.html", data = data)

@app.route("/create_warehouse", methods=["POST"])
def create_warehouse():
    if 'user_id' not in session:
        return redirect('/')
    if not Warehouse.validate_warehouse(request.form):
        return redirect('/new_warehouse')
    data = {
        "whs_name": request.form["whs_name"]
    }
    id = Warehouse.insert_whs(data)
    return redirect('/dashboard')

@app.route("/new_stockin/<int:id>") #per warehouse
def stock_in(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "whs_id": id,
        "user_id": session['user_id']
        }
    warehouse = Warehouse.get_all_whs_dropdown()
    items = Inventory.get_all_items()
    return render_template("stock_in.html", data = data, items = items, warehouse = warehouse)

@app.route("/create_stock_in", methods=["POST"]) #per warehouse
def create_stock_in():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "item_id": request.form["item_id"],
        "quantity": request.form["quantity"],
        "whs_id": request.form["whs_id"]
    }
    if not Warehouse.validate_stockin(request.form):
        return redirect(f"/new_stockin/{int(data['whs_id'])}")
    id = Warehouse.insert_stock_in(data)
    Warehouse.update_inventory(data)
    return redirect('/dashboard')
