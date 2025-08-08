from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.models_user import User
from flask_app.models.models_inventory import Inventory
from flask_app.models.models_warehouse import Warehouse
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"]
        }
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data['pw_hash'] = pw_hash
    id = User.insert_user(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route("/login", methods=["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'email': request.form['email'],
        'password': request.form['password']
        }
    user = User.get_user_details_by_email(data)
    session['user_id'] = user['id']
    print('login', session['user_id'] )
    return redirect('/dashboard')

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    warehouse = Warehouse.get_all_whs_dropdown()
    user = User.get_user_details_by_id(data)
    return render_template("dashboard.html", warehouse = warehouse, user = user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
