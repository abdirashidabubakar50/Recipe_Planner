from flask import Blueprint,render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_required, current_user, login_user, logout_user
from app.models.user import User
from app.models.forms import RegisterForm, LoginForm

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

            flash('Registration successful! please log in.' 'success')
            return redirect(url_for('auth.login'))

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
                return redirect(url_for('api.dashboard'))
            else:
                errors['username'] = "Incorrect username or password"
                return render_template('login.html', errors=errors)
    return render_template('login.html', errors=errors,  form=form)



"""logout the user"""
@auth.route('/logout')
@login_required
def logout():
    """clear the session data"""
    logout_user()

    """Redirect the user to the login page or homepage"""
    return redirect(url_for('auth.login'))
