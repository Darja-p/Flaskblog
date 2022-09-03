from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from application import db
from application.models import User, BlogPost
from application.users.forms import LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm
from application.users.utils import send_reset_email
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint('users', __name__)

@users.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    # # print("first:",[arg for arg in request.args])
    next_page = request.args.get('next')
    #
    if request.method == "POST" :
        user_email = request.form.get('email')
        user = User.query.filter_by(email=user_email).first()
        if not user:
            flash("That email does not exist, please try again.")
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            print(current_user.id)
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash('Login unsuccessful. Please check password and try again.')
    return render_template("login.html", form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/register', methods = ["GET", "POST"])
def register():
    form = RegisterForm()
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    if form.validate_on_submit():
        hashed_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256',salt_length=8)
        new_user = User (email = request.form['email'],password = hashed_password,name= request.form['name'] )
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('main.home'))
        except IntegrityError:
            flash("User with this email already exists. Please log in",'warning')
            return redirect(url_for('users.login'))
    return render_template("register.html", form=form)


@users.route('/reset-password', methods = ["GET", "POST"])
def reset_password():
    form = RequestResetForm()
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been send with instructions")
        return redirect(url_for("users.login"))
    return render_template("request_reset.html", form=form)

@users.route('/reset-password/<secret>', methods = ["GET", "POST"])
def reset_token(secret):
    print(secret)
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    user = User.verify_reset_token(token=secret)
    if user is None:
        flash('This link has expired')
        return redirect(url_for("users.reset_password"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated", 'warning')
        return redirect(url_for('users.login'))
    return render_template("request_reset.html", form=form)
