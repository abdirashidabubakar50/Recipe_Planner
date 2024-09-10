from flask import Blueprint, render_template, request, current_app
from flask import flash, redirect, url_for
import requests
from flask_login import login_required, current_user, login_user, logout_user
from app.models.user import User
from app.models.all_recipes import AllRecipe
from app.models.meal_plan import Meal_plan
from app.models.recipe import SavedRecipe
from app.helpers.helpers import get_recipes
from app.models.forms import AddToMealPlanForm, UpdateuserForm
from app import db
import json


api = Blueprint('api', __name__)


"""Landing page route"""
@api.route('/home')
def home():
    return render_template('home.html')


""" User dahsboard """
@api.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    """
    Render the dashboard template with the fetched data

    """
    user_id = current_user.id
    # saved_recipe = saved_recipes(user_id)
    saved_recipes = SavedRecipe.query.filter_by(user_id=current_user.id).all()
    total_saved_recipes = len(saved_recipes)
    print(total_saved_recipes)
    recommended_recipes = get_recipes(db=db ,user=current_user)
    return render_template(
        'dashboard.html',
        recommended_recipes=recommended_recipes,
        total_saved_recipes=total_saved_recipes,
        user=current_user,
        user_id=current_user.id
    )

"""search recipe route"""
@api.route('/search_recipe', methods=['GET', 'POST'])
@login_required
def search_recipe():
    keyword = request.args.get('query', '').strip()
    print(f"Search keyword received: {keyword}")
    recipes = get_recipes(db=db, keyword=keyword, user=current_user)
    print(f"Recipes returned: {[recipe.name for recipe in recipes]}")
    return render_template(
        'dashboard.html',
        recipes=recipes,
        user=current_user,
        user_id=current_user.id
    )


"""Displays the recipe details"""
@api.route('/recipe_detail/<int:recipe_id>', methods=['GET'])
@login_required
def recipe_detail(recipe_id):
    recipe = AllRecipe.query.get_or_404(recipe_id)
    return render_template(
        'recipe_detail.html',
        recipe=recipe,
        user=current_user,
        user_id=current_user.id
    )


@api.route('/meal_plan', methods=['GET'])
@login_required
def meal_plan():
    user = current_user
    recipe = AllRecipe.query.get_or_404(recipe_id)
    meal_plans= Meal_plan.query.filter_by(user_id=user.id).all()
    for recipe in meal_plans.recipes:
        print(recipe.name)
        print(recipe.image_url)
    return render_template(
        'meal_plan.html',
        user=current_user,
        meal_plans=meal_plans,
        user_id=current_user.id
    )


"""Saves the recipe"""
@api.route('/save_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    """Save the recipe to the user's meal plan."""
    user_id = current_user.id
    recipe = AllRecipe.query.get_or_404(recipe_id)

    """ Created a saved Recipe instacnce"""
    saved_recipe = SavedRecipe(
        id=recipe_id,
        user_id = user_id,
        name=recipe.name,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        diet_type=recipe.diet_type,
        allergies=recipe.allergies,
        image_file=recipe.image_url,
        nutrients=recipe.nutrients
    )
    if saved_recipe.save():
        message = 'Recipe Saved'
        flash(message, 'success')
        return redirect(url_for(
            'api.recipe_detail',
            recipe_id=recipe.id,
            user_id=user_id
        ))
    else:
        flash("Recipe already exists in your collection")
        return redirect(url_for(
            'api.recipe_detail',
            recipe_id=recipe.id,
            user_id=user_id
        ))


"""display the saved recipes"""
@api.route('/saved_recipes/<int:user_id>')
@login_required
def saved_recipes(user_id):

    if user_id != current_user.id:
        abort(403)
    # query the user's saved recipes
    saved_recipes = SavedRecipe.query.filter_by(user_id=current_user.id).all()

    if not saved_recipes:
        flash("No saved Recipes Found", "info")
    return render_template(
        'saved_recipes.html',
        saved_recipes=saved_recipes,
        user_id=current_user.id, user=current_user
    )


""" Adds the recipe to meal plan"""
@api.route('/add_to_mealplan/<int:recipe_id>', methods=['POST'])
@login_required
def add_to_mealplan(recipe_id):
    recipe = AllRecipe.query.get_or_404(recipe_id)
    meal_plan = Meal_plan.query.filter_by(user_id=current_user.id).first()

    if not meal_plan:
        # Create a new meal plan if none exists
        meal_plan = Meal_plan(user_id=current_user.id, title="My Meal Plan")
        db.session.add(meal_plan)
        db.session.commit()

    # Add recipe to the meal plan
    meal_plan_added = meal_plan.recipes.append(recipe)  
    print(meal_plan.recipes)
    for recipe in meal_plan.recipes:
        print(f"Recipe: {recipe}")
        print(f"Name: {getattr(recipe, 'name', 'Attribute not found')}")
        print(f"Title: {getattr(recipe, 'title', 'Attribute not found')}")
        print(f"Image URL: {getattr(recipe, 'image_url', 'Attribute not found')}")
    db.session.commit()
    flash('Recipe added to your meal plan!', 'success')
    return redirect(url_for('api.recipe_detail', recipe_id=recipe.id, meal_plan_added=meal_plan_added))



"""Display the user's profile and  update"""
@api.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    """Display and update the user's profile"""
    form = UpdateuserForm()
    user=current_user
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.username = request.form.get(
                'username',
                current_user.username
            )
            New_password = request.form.get('password', current_user.password)
            current_user.email = request.form.get('email', current_user.email)
        updated_profile = User(
            username=current_user.username,
            email=current_user.username
        )
        updated_profile.update()
        print("updated the profile")
        flash(
            "The profile has been updated successfully!",
            "success"
        )
    return render_template(
        'profile.html',
        user=current_user,
        user_id=current_user.id,
        form=form
    )
