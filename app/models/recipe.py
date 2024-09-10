from .. import db
from datetime import datetime
"""
This module defines the class Recipe 

"""

class SavedRecipe(db.Model):
    """This class defines Recipe with various attributes"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    diet_type = db.Column(db.String(150))
    allergies = db.Column(db.JSON)
    image_file = db.Column(db.String(120), nullable=False)
    nutrients = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Recipe {self.name}>'
    
    def save(self):
        """save the recipe to the database"""
        existing_recipe = SavedRecipe.query.filter_by(user_id=self.user_id, name=self.name).first()

        if existing_recipe:
            print(f"Recipe '{self.name}' already exists in user's saved recipes '{self.user_id}'")
            return False
        else:
            try:
                db.session.add(self)
                db.session.commit()
                return True
            except Exception as e:
                print(f"Error saving recipe: {e}")
                db.session.rollback()
                return False
    
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
        if diet_type is not None:
            self.diet_type = diet_type
        db.session.commit()
    def delete(self):
        """Delete the Recipe from the database"""
        db.session.delete(self)
        db.session.commit()