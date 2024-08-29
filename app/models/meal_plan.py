from .. import db
from datetime import datetime
"""
This module defines meal plan class. A meal plan is created and
the details can be updated or deleted

"""

class Meal_plan(db.Model):
    """ This class defines Meal_plan by various attributes"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    groceries = db.relationship('Grocery', backref='meal_plan', lazy=True,cascade='all, delete-orphan')

    def __repr__(self):
        return f"'{self.title}, Created On {self.created_at}"
    
    def save(self):
        """saves the meal plan to the database"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, title=None, description=None, start_date=None, end_date=None):
        """updates the meal plan and saves the new plan in the database"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        db.session.commit()
    
    def delete(self):
        """delete the meal plan from the database"""
        db.session.delete(self)
        db.session.commit()
