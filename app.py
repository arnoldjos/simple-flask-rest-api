import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT
from flask_migrate import Migrate
from db import db

from security import authenticate, identity
from api import api_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "1234567")
app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///G:\tutorials\flask-rest-api\data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# SQLAlchemy
db.init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}})
JWT(app, authenticate, identity)
Migrate(app, db)

# blueprints
app.register_blueprint(api_bp)

if __name__ == "__main__":
    load_dotenv(verbose=True)
    app.run()
