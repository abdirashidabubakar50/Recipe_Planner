from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_wtf import CSRFProtect
from authlib.integrations.flask_client import OAuth
oauth = OAuth()

from flask_login import LoginManager

login_manager = LoginManager()
csrf = CSRFProtect()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Initialize CSRF protection
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from app.models import user, recipe, meal_plan, grocery_list, all_recipes, mealPlanRecipe, scheduled_recipes
        db.create_all()

        # initialize OAuth for Google Login
        oauth.init_app(app)
        google = oauth.register(
            name='google',
            client_id=app.config['GOOGLE_CLIENT_ID'],
            client_secret=app.config['GOOGLE_CLIENT_SECRET'],
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            authorize_params=None,
            access_token_url='https://oauth2.googleapis.com/token',
            access_token_params=None,
            refresh_token_url=None,
            redirect_uri='http://localhost:5000/login/google/authorize',
            client_kwargs={'scope': 'openid profile email'}
        )
        # Register Routes
        from app.auth.routes import auth
        from app.api.routes import api
        app.register_blueprint(auth)
        app.register_blueprint(api)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))