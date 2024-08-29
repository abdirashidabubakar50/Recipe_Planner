from .. import db
from datetime import datetime
"""
This module defines the class Recipe 

"""

class Recipe(db.Model):
    """This class defines Recipe with various attributes"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    diet_type = db.Column(db.String(50))
    allergies = db.Column(db.JSON)

    def __repr__(self):
        return f',Recipe {self.name}>'
    
    def save(self):
        """save the recipe to the database"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, name=None, ingredients=None, instructions=None, diet_type=None, allergies=None):
        """update the recipe's details"""
        if name is not None:
            self.name = name
        if ingredients is not None:
            self.ingredients = ingredients
        if instructions is not None:
            self.instructions = instructions
        if allergies is not None:
            self.allergies = allergies
        db.session.commit()
    def delete(self):
        """Delete the Recipe from the database"""
        db.session.delete(self)
        db.session.commit()