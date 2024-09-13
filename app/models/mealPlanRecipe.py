from .. import db

class MealplanRecipe(db.Model):
    """This class defines AllRecipe with various attributes."""
    __tablename__ = 'mealplan_recipe'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plan.id'), primary_key=True, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('all_recipe.id'), primary_key=True, nullable=False)
   