from flask import Flask
from flask_pymongo import pymongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "66793263b974204e75f88e78ad737bcda3cb"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# cluster = "mongodb+srv://Manish:Consultadd7897@cluster1.g3pif.mongodb.net/Mydatabase?retryWrites=true&w=majority"
# client = pymongo.MongoClient(cluster)
# db = client.Mydatabase
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from first import route

