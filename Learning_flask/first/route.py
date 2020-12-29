from flask import render_template, url_for, redirect, flash
from first.forms import RegistrationForm, LoginForm
from first import app, db, bcrypt
from first.model import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/register", methods=['Get', 'POST'])
def registration():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if form.validate_on_submit():
        flash(f'Account has been created for {form.name.data}!', 'success')

        # db.app1.insert_one({'Name': form.name.data, 'Username': form.username.data, 'Email': form.email.data,
        #                     'Password': bcrypt.generate_password_hash(form.password.data).decode('utf-8')})
        # return render_template('dashboard.html')

        var1 = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            var = User(name=form.name.data, username=form.username.data, email=form.email.data, password=var1)
            db.session.add(var)
            db.session.commit()
            return render_template('dashboard.html')
    return render_template('Registration.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('login unsuccessful, Please check email or password', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
