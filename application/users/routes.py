from flask import render_template, redirect, url_for, request, Blueprint, abort
from flaskcarleasing.models import Car, User
from flaskcarleasing.config import db, MODERATOR_TOKEN
from users.forms import RegisterForm, LoginForm, UpdateForm
import hashlib
from flask import flash
from flask_login import login_user, current_user, logout_user


users = Blueprint('users', __name__, template_folder='templates')


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You have already logged in')
        return redirect(url_for('main.index'))

    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data

        password = form.password.data
        password = hashlib.md5(password.encode()).hexdigest()

        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data

        user_info = {
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
        }

        user = User(**user_info)
        
        db.session.add(user)
        db.session.commit()

        flash('You Now May Log In')

        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    validation = None

    if current_user.is_authenticated:
        flash('You are logged in')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        password = hashlib.md5(password.encode()).hexdigest()

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user, form.remember_me.data)
            flash('You Have Logged In')
            return redirect(url_for('main.index'))

    return render_template('users/login.html', form=form, validation=validation)


@users.route('/logout')
def logout():
    if not current_user.is_authenticated:
        abort(401)

    logout_user()
    return redirect(url_for('main.index'))


@users.route('/account', methods=['GET', 'POST'])
def account():
    if not current_user.is_authenticated:
        abort(401)

    form = RegisterForm()
    form.submit.label.text = 'Update user info'

    if request.method == 'GET':
        form.username.data = current_user.username
        form.phone_number.data = current_user.phone_number
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.phone_number = form.phone_number.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data

        if form.moderator_token.data == MODERATOR_TOKEN:
            current_user.superuser = True
            flash('Successfully activated moderator token. You now can create/update/delete items from the application database.')
            print(current_user)

        db.session.commit()

        flash('User info has been successfully changed')
        redirect(url_for('users.account'))

    return render_template('users/account.html', form=form)


@users.route('/contracts', methods=['GET', 'POSt'])
def contracts():
    if not current_user.is_authenticated:
        abort(401)

    user = current_user
    return render_template('users/contracts.html', user=user)