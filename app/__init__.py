from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.models import user, recipe, meal_plan, grocery_list
        db.create_all()


        # Register Routes
        from app.auth.routes import auth
        from app.api.routes import api
        app.register_blueprint(auth)
        app.register_blueprint(api)

    return app
