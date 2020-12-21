from flask import Flask, request, jsonify, flash, session, url_for, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_pymongo import pymongo
from pymongo import MongoClient
# from passlib.hash import sha256_crypt
from flask_bcrypt import Bcrypt
from bson.json_util import dumps
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = "abc/abc/bcd/bcd"
basedir = os.path.abspath(os.path.dirname(__file__))
cluster = "mongodb+srv://Manish:Consultadd7897@cluster1.g3pif.mongodb.net/Mydatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(cluster)
db = client.Mydatabase
# user_collection = pymongo.collection.Collection(db, 'user_collection')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'new.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)


# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(100))
#     lastname = db.Column(db.String(100))
#     username = db.Column(db.String(100), unique=True)
#     email = db.Column(db.String(180), unique=True)
#     password = db.Column(db.String(100))
#
#     def __init__(self, firstname, lastname, username, email, password):
#         self.firstname = firstname
#         self.lastname = lastname
#         self.username = username
#         self.email = email
#         self.password = password
#
#
# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'firstname', 'username', 'email', 'password')
#
#
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)


@app.route("/")
def hello():
    message = "Hello Consultadd"
    return render_template('home.html', message=message)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/dashboard')

    return wrap


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')


def start_session(user):
    del user['password']
    session['logged_in'] = True
    session['user'] = str(user)
    dumps(user)
    return redirect(url_for('hello'))


@app.route("/login", methods=["GET", "POST"])
def login():
    # if request.method == "POST":
    user = db.app1.find_one({"username": request.form.get('uname'), "password": request.form.get('psw')})

    if user and Bcrypt.check_password_hash(request.form.get('psw'), user['password']):

        return start_session(user)
    else:
        print("wrong creds")
        return render_template('login.html')


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('psw')

        new_user = {"firstname": firstname, "lastname": lastname, "username": username, "email": email,
                    'password': bcrypt.generate_password_hash(password).decode('utf-8')}
        # db.collection.insert_one(new_user)
        if db.app1.find_one({"email": new_user['email']}):
            flash('email already exists')
            return render_template("new.html")
        else:
            db.app1.insert_one(new_user)
            return start_session(new_user)

        # db.session.add(new_user)
        # db.session.commit()

        # return user_schema.jsonify(new_user)
    else:
        return render_template('Registration.html')


@app.route("/users", methods=['GET'])
def get_user():
    # all_users = Users.query.all()
    # result = users_schema.dump(all_users)
    # return jsonify(result)
    var = db.collection.find({})
    return var


@app.route("/regis/<id>", methods=['GET'])
def get_user_id(id):
    users_id = Users.query.get(id)
    result = user_schema.dump(users_id)
    return jsonify(result)


@app.route('/logout')
def log_out():
    session.clear()
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
