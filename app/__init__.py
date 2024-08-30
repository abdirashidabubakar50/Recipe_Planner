from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

from flask_login import LoginManager

login_manager = LoginManager()


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    with app.app_context():
        from app.models import user, recipe, meal_plan, grocery_list
        db.create_all()


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