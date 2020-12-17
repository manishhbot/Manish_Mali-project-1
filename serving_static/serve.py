from flask import Flask, request, jsonify
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'new.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(180), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'username', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/")
def hello():
    message = "Hello Consultadd"
    return render_template('home.html', message=message)


@app.route("/login")
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('psw')

        new_user = Users(username, password)

        db.session.add(new_user)
        db.session.commit()
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('psw')

        new_user = Users(firstname, lastname, username, email, password)

        db.session.add(new_user)
        db.session.commit()

        # return user_schema.jsonify(new_user)
        return render_template("login.html")
    else:
        return render_template("Registration.html")


@app.route("/regis", methods=['GET'])
def get_user():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route("/regis/<id>", methods=['GET'])
def get_user_id(id):
    users_id = Users.query.get(id)
    result = user_schema.dump(users_id)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
