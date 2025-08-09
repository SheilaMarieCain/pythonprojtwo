from flask_app import app
from flask_app.controllers import controllers_users
from flask_app.controllers import controllers_inventories
from flask_app.controllers import controllers_orders
from flask_app.controllers import controllers_reports
from flask_app.controllers import controllers_customers
from flask_app.controllers import controllers_warehouses

app.secret_key = 'keep it secret, keep it safe' # set a secret key for security

if __name__ == "__main__":
    app.run(debug=True)
