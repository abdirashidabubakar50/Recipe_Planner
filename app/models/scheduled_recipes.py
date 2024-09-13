from .. import db
from datetime import datetime

class ScheduledRecipes(db.Model):
    __tablename__ = 'scheduled_recipes'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('all_recipe.id'), nullable=False)  # Fixed the foreign key reference
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    # Define the relationships with AllRecipe and Meal_plan
    recipe = db.relationship('AllRecipe', backref='scheduled_recipes', lazy=True)
    meal_plan = db.relationship('Meal_plan', backref='scheduled_recipes', lazy=True)

    def __repr__(self):
        return f"<ScheduledRecipe(recipe_id={self.recipe_id}, start_time={self.start_time}, end_time={self.end_time})>"
