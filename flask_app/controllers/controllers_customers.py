from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.models_customer import Customer
from flask_app.models.models_user import User
from flask import flash

@app.route("/new_customer")
def new_customer():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("new_customer.html")

@app.route("/create_customer", methods=["POST"])
def create_customer():
    if 'user_id' not in session:
        return redirect('/')
    if not Customer.validate_customer(request.form):
        return redirect('/new_customer')
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "contact_no": request.form["contact_no"]
    }
    id = Customer.insert_customer(data)
    return redirect('/dashboard')
