from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.models_report import Report
from flask_app.models.models_user import User
from flask_app.models.models_report_order import Report_Order
from flask import flash

@app.route("/sales_report")
def view_sales():
    if 'user_id' not in session:
        return redirect('/')
    sales = Report.get_sales_report()
    return render_template("sales_report.html", sales = sales)

@app.route("/reorder_items")
def reorder_items():
    if 'user_id' not in session:
        return redirect('/')
    items = Report.reorder_items()
    return render_template("reorder_items.html", items = items)

@app.route("/orders_by_item")
def orders_by_item():
    if 'user_id' not in session:
        return redirect('/')
    orders = Report_Order.get_orders_by_item()
    return render_template("orders_by_item.html", orders = orders)

@app.route("/items_by_order")
def items_by_order():
    if 'user_id' not in session:
        return redirect('/')
    items = Report_Order.get_items_by_order()
    return render_template("items_by_order.html", items = items)
