from .. import db
from datetime import datetime
"""
This module define a class grocery list that returns a grocery list for a recipe

"""


class Grocery(db.Model):
    """
    This class defines grocery list with various attributes. Returns a grocery list for a recipe

    """
    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'), nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.String(60), nullable=False)
    checked = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"'{self.item_name}'"
    
    def save(self):
        """saves the grocery to the database"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """updates the attributes of the Grocery instance with the given keyword arguments
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    def delete(self):
        """deletes the grocery form the database"""
        db.session.delete(self)
        db.session.commit()
