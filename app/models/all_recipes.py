from .. import db
from datetime import datetime
"""
This module defines the class Recipe 

"""

class AllRecipe(db.Model):
    """This class defines Recipe with various attributes"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    diet_type = db.Column(db.String(150))
    allergies = db.Column(db.JSON)
    image_url = db.Column(db.String(255))
    nutrients = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Recipe {self.name}>'
    
    def save(self):
        """save the recipe to the database"""
        db.session.add(self)
        db.session.commit()
