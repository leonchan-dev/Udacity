from flask import Flask
from flask_cors import CORS
from models import *


def create_app():
    app = Flask(__name__)
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    return app
app = create_app()

db = SQLAlchemy(app)
migrate = Migrate(app, db)