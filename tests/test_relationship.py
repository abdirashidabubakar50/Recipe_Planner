from app import create_app, db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.meal_plan import Meal_plan 
from app.models.grocery_list import Grocery  # Importing the Grocery model

def test_relationship():
    app = create_app()
    with app.app_context():
        Recipe.query.delete()
        Grocery.query.delete()
        Meal_plan.query.delete()
        User.query.delete()
        db.session.commit()
        # Create a new user with a password
        user = User(username='John Doe', email='john@example.com', password='password123', preferences={}, allergies={})
        db.session.add(user)
        db.session.commit()

        # Create a recipe for this user
        recipe = Recipe(user_id=user.id, name='Pasta', ingredients={}, instructions='Boil pasta.')
        db.session.add(recipe)
        db.session.commit()

        # Create a meal plan for this user
        meal_plan = Meal_plan(user_id=user.id, description='VEGAN', title='gluten free')
        db.session.add(meal_plan)
        db.session.commit()

        # Create a grocery item for this meal plan
        grocery = Grocery(meal_plan_id=meal_plan.id, item_name='Tomatoes', quantity='2 kg', checked=False)
        db.session.add(grocery)
        db.session.commit()

        # Fetch and print relationships
        user_recipes = User.query.get(user.id).recipes
        user_meal_plans = User.query.get(user.id).meal_plans
        meal_plan_groceries = Meal_plan.query.get(meal_plan.id).groceries

        assert len(user_recipes) == 1
        assert len(user_meal_plans) == 1
        assert len(meal_plan_groceries) == 1

        print("User, Recipe, MealPlan, and Grocery relationships are working correctly!")

if __name__ == "__main__":
    test_relationship()


