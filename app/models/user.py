from .. import db
from datetime import datetime
from flask_login import UserMixin
""" This module defines the class user."""

class User(UserMixin,db.Model):
    """This class defines User with various attributes"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    preferences = db.Column(db.JSON, nullable=True)
    allergies = db.Column(db.JSON, nullable=True)
    recipes = db.relationship('SavedRecipe', backref='user', cascade='all, delete-orphan')
    meal_plans = db.relationship('Meal_plan', backref='user', lazy=True)


    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"


    def save(self):
        """save the user to the database"""
        db.session.add(self)
        db.session.commit()


    def update(self, username=None, email=None, preference=None, allergies=None):
        """ update the userr's information"""
        if username is not None:
            self.username = Name
        if email is not None:
            self.email = email
        if preference is not None:
            self.preference = preference
        if allergies is not None:
            sefl.allergies = allergies
        db.session.commit()


    def delete(self):
        """delete the user from the database"""
        db.session.delete(self)
        db.session.commit()

