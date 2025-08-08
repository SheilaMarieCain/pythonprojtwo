from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.models_inventory import Inventory
from flask_app.models.models_user import User
from flask import flash

@app.route("/new_item")
def new_item():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id']
        }
    return render_template("new_item.html", data = data)

@app.route("/create_item", methods=["POST"])
def create_item():
    if 'user_id' not in session:
        return redirect('/')
    if not Inventory.validate_item(request.form):
        return redirect('/new_item')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "unit_price": request.form["unit_price"],
        "selling_price": request.form["selling_price"],
        "reorder_level": request.form["reorder_level"],
        "user_id": session['user_id']
    }
    id = Inventory.insert_item(data)
    return redirect('/dashboard')

@app.route("/edit_item/<int:id>")
def edit_item(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    item = Inventory.edit_one_item(data)
    return render_template("edit_item.html", item = item)

@app.route("/update_item", methods=["POST"])
def update_item():
    if 'user_id' not in session:
        return redirect('/')
    if not Inventory.validate_item(request.form):
        return redirect('/new_item')
    data = {
        "id": request.form["id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "unit_price": request.form["unit_price"],
        "selling_price": request.form["selling_price"],
        "reorder_level": request.form["reorder_level"]
    }
    Inventory.update_item(data)
    return redirect('/dashboard')

@app.route("/view_item/<int:whs_maintenance_id>/<int:id>") #per warehouse
def view_item(whs_maintenance_id, id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "whs_maintenance_id": whs_maintenance_id,
        "id": id,
        "user_id": session['user_id']
    }
    item = Inventory.get_one_item(data)
    return render_template("view_item.html", item = item)

@app.route("/show_all_items/<int:id>") #per warehouse
def show_all_items(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "whs_id": id,
        "user_id": session['user_id']
    }
    items = Inventory.get_all_items_per_whs(data)
    user = User.get_user_details_by_id(data)
    return render_template("show_all_items.html", data = data, items = items, user = user)

@app.route("/delete_choose_item")
def delete_choose_item():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "user_id": session['user_id']
    }
    items = Inventory.get_all_items_not_in_whs()
    user = User.get_user_details_by_id(data)
    return render_template("delete_items.html", data = data, items = items, user = user)

@app.route("/delete_item/<int:id>")
def delete_item(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    Inventory.delete_item(data)
    return redirect('/dashboard')
