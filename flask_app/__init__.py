from flask import Flask

app = Flask(__name__)

from server import app as application
if __name__ == "__main__":
    application.run()
