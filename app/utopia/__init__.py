from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSON_SORT_KEYS'] = False
app.config['DB_HOST'] = os.getenv('DB_HOST')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DB_USER'] = os.getenv('DB_USER')
app.config['DB_USER_PASSWORD'] = os.getenv('DB_USER_PASSWORD')
app.config['DB'] = os.getenv('DB')
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_CSRF_IN_COOKIES"] = True
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config['JSON_SORT_KEYS'] = False



from utopia import booking_controller, error_handler
