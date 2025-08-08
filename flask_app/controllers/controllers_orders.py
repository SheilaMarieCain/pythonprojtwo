from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.models_order import Order
from flask_app.models.models_user import User
from flask_app.models.models_customer import Customer
from flask_app.models.models_inventory import Inventory
from flask_app.models.models_report_order import Report_Order
from flask import flash
from datetime import datetime

@app.route("/new_order/<int:id>") #per warehouse
def new_order(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "whs_id": id,
        "user_id": session['user_id'],
        "customer_id": 0
        }
    customers = Customer.get_all_customers()
    items = Inventory.get_all_items_per_whs(data)
    return render_template("new_order.html", data = data, customers = customers, items = items)

@app.route("/create_order_hdr", methods=["POST"])
def create_order_hdr():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "order_date": request.form["order_date"],
        "whs_id": request.form["whs_id"],
        "customer_id": request.form["customer_id"],
        "remarks": request.form["remarks"],
        "user_id" : session['user_id'],
        "item_id": request.form["item_id"],
        "selling_price": request.form["selling_price"],
        "stock_on_hand": request.form["stock_on_hand"],
        "quantity": request.form["quantity"],
        "amount": request.form["amount"],
        "order_hdr_id": request.form['order_hdr_id']
    }
    if not Order.validate_order(request.form):
        return redirect(f"/new_order/{int(data['whs_id'])}")
    if len(data['order_hdr_id']) > 0:
        order_hdr_id = data['order_hdr_id'] #use current order number for the additional items
        Order.update_order_hdr(data)
    else:
        order_hdr_id = Order.insert_order_hdr(data) #generate new order number
    data = {
        "order_hdr_id": order_hdr_id,
        "whs_id": request.form["whs_id"],
        "customer_id": request.form["customer_id"],
        "order_date": request.form["order_date"],
        "remarks": request.form["remarks"],
        "item_id": request.form["item_id"],
        "quantity": request.form["quantity"],
        "selling_price": request.form["selling_price"],
        "amount": request.form["amount"]
    }
    order_dtl_id = Order.insert_order_dtl(data)
    data_1 = {"order_dtl_id": order_dtl_id,
            "item_id": request.form["item_id"]}
    Order.insert_items_has_order_dtl(data_1)
    Order.update_inventory(data)
    if request.form.get('add_another_item') != 'Yes':  #No
        print('new_order')
        return redirect(f"/new_order/{int(data['whs_id'])}")
    else:
        print('nadditional_item_in_current_order')
        return redirect(f"/additional_item_in_current_order/{int(data['whs_id'])}/{int(data['customer_id'])}/{int(data['order_hdr_id'])}/{data['order_date']}/{data['remarks']}")

@app.route("/additional_item_in_current_order/<int:id>/<int:customer_id>/<int:order_hdr_id>/<order_date>/<remarks>") #whsid, customer_id
def additional_item_in_current_order(id, customer_id, order_hdr_id, order_date, remarks):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "whs_id": id,
        "customer_id": customer_id,
        "order_hdr_id": order_hdr_id,
        "order_date": datetime.strptime(order_date, "%Y-%m-%d").date(),
        "remarks": remarks,
        "user_id": session['user_id']
        }
    customers = Customer.get_all_customers()
    items = Inventory.get_all_items_per_whs(data)
    print('order_hdr_id', data['order_hdr_id'])
    return render_template("new_order.html", data = data, customers = customers, items = items)
