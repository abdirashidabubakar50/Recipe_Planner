from flask import Blueprint,render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, oauth
from flask_login import login_required, current_user, login_user, logout_user
from app.models.user import User
from app.models.forms import RegisterForm, LoginForm
from authlib.integrations.flask_client import OAuth
from flask import url_for
import json
import secrets

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form =RegisterForm()
    errors = {}
    if form.validate_on_submit:
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get("confirm password")
            diet_type = request.form.get('diet_type')
            allergies = request.form.get('allergies')


            if not username:
                errors['username'] = "Username is required"
            if password != confirm_password:
                errors['confirm_password'] = "Passwords do not match"
            if not email:
                errors['email'] = "Email is required"
            if not password:
                errors['password'] = "Password is required"
            if len(password) < 8:
                errors['password'] = "Password must be atleast 8 characters long"

            if errors:
                return render_template('register.html', errors=errors, username=username, email=email, form=form)
            
            #check if the username or email already exists
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                if existing_user.username == username:
                    errors['username'] = "Username already exists"
                if existing_user.email == email:
                    errors['email'] = "Email address already exists"
                return render_template('register.html', errors=errors, username=username, email=email, form=form)

            # create a new user
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                preferences=diet_type,
                allergies=allergies
            )
            new_user.save()
            print("registration was successful")
            flash('Registration successful! please log in.' 'success')
            return redirect(url_for('auth.login'))
        else:
            print("registration was not successful")
    return render_template('register.html', errors=errors, form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = {}
    if form.validate_on_submit():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            """ check if the user exists """
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                """set session data"""
                login_user(user)
                flash('Login successful!', 'successful')
                return redirect(url_for('api.dashboard', user_id=current_user.id, username=current_user.username))
            else:
                errors['username'] = "Incorrect username or password"
                return render_template('login.html', errors=errors, form=form)
    return render_template('login.html', errors=errors,  form=form)



""" google login route """
@auth.route('/login/google')
def google_login():
    nonce = secrets.token_urlsafe(16)
    session['nonce'] = nonce

    print(f"Generated Nonce: {nonce}")
    redirect_uri = url_for('auth.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

"""google OAuth2 callback"""
@auth.route('/login/google/authorize')
def google_authorize():
    try:
        token = oauth.google.authorize_access_token()
        nonce = session.get('nonce', None)

        if not nonce:
            print('Nonce missing from session', 'error')
            return redirect(url_for('auth.login'))
        user_info = oauth.google.parse_id_token(token, nonce=nonce)

        if user_info:
            user = User.query.filter_by(email=user_info['email']).first()

            if user:
                """if user exists, log them in"""
                login_user(user)
                return redirect(url_for('api.dashboard'))
            else:
                """if user doesn't exist, create a new user"""
                new_user = User(
                    username=user_info['name'],
                    email = user_info['email'],
                    password=generate_password_hash('randompassword', method='pbkdf2:sha256')
                )
                new_user.save()
                login_user(new_user)

                print('Login successful', 'success')
                return redirect(url_for('api.dashboard'))
        else:
            print('failed to login with google', 'error')
            return redirect(url_for('auth.login'))
    except Exception as e:
        print(f'Error during login with google: {str(e)}', 'error')
        return redirect(url_for('auth.login'))


"""logout the user"""
@auth.route('/logout')
@login_required
def logout():
    """clear the session data"""
    logout_user()

    """Redirect the user to the login page or homepage"""
    return redirect(url_for('auth.login'))
