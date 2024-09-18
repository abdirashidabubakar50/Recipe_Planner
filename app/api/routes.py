from flask import Blueprint, render_template, request, current_app, jsonify
from flask import flash, redirect, url_for
import requests
from flask_login import login_required, current_user, login_user, logout_user
from app.models.user import User
from app.models.all_recipes import AllRecipe
from app.models.meal_plan import Meal_plan
from app.models.recipe import SavedRecipe
from app.helpers.helpers import get_recipes
from app.models.scheduled_recipes import ScheduledRecipes
from app.models.mealPlanRecipe import MealplanRecipe
from app.models.forms import AddToMealPlanForm, UpdateuserForm
from app import db
import json


api = Blueprint('api', __name__)


"""Landing page route"""
@api.route('/')
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
        recipe_id = recipe.id,
        recipe=recipe,
        user=current_user,
        user_id=current_user.id
    )


@api.route('/meal_plan', methods=['GET'])
@login_required
def meal_plan():
    user = current_user
    meal_plan = Meal_plan.query.filter_by(user_id=user.id).first()

    unscheduled_recipes = [
        recipe for recipe in meal_plan.recipes 
        if not any(sr.recipe_id == recipe.id for sr in meal_plan.scheduled_recipes)
    ]

    # Fetch scheduled recipes
    scheduled_recipes = ScheduledRecipes.query.join(Meal_plan).filter(Meal_plan.user_id == current_user.id).all()
    # Convert scheduled recipes to JSON for FullCalendar
    calendar_events = [{
        'title': scheduled_recipe.recipe.name,
        'start': scheduled_recipe.start_time.isoformat(),
        'end': scheduled_recipe.end_time.isoformat(),
        'url': url_for('api.recipe_detail', recipe_id=scheduled_recipe.recipe_id)
    } for scheduled_recipe in scheduled_recipes]

    print("Calendar Events JSON:", json.dumps(calendar_events))
    return render_template(
        'meal_plan.html',
        scheduled_recipes = scheduled_recipes,
        user=current_user,
        recipes=unscheduled_recipes,
        user_id=current_user.id,
        calendar_events=calendar_events,
        meal_plan_id=meal_plan.id
    )


@api.route('/schedule_recipe', methods=['POST'])
@login_required
def schedule_recipe():
    data = request.get_json()
    print(f"Recieved data: {data}")
    recipe_id = data.get('recipe_id')
    meal_plan_id = data.get('meal_plan_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')


    if not recipe_id or not start_time or not end_time or not meal_plan_id:
        return {"success":False, "message": "Missing required data."}, 400
    
    meal_plan = MealplanRecipe.query.filter_by(meal_plan_id=meal_plan_id, recipe_id=recipe_id).first()
    if not meal_plan:
        return jsonify({'error': 'Meal Plan ID is required'}), 400
    # Ensure the recipe exists
    recipe = AllRecipe.query.get_or_404(recipe_id)

    # Create a scheduled recipe instance
    scheduled_recipe = ScheduledRecipes(
        meal_plan_id = meal_plan_id,
        recipe_id=recipe.id,
        start_time=start_time,
        end_time=end_time
    )

    db.session.add(scheduled_recipe)
    db.session.commit()

    # Return success response
    return {
        'success': True,
        # 'meal_plan_id': meal_plan.id,
        'recipe_name': recipe.name,
        'start_time': start_time,
        'end_time': end_time
    }


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
        return redirect(url_for('api.recipe_detail', recipe_id=recipe.id))
    if recipe in meal_plan.recipes:
        flash("Recipea already in the meal Plan!", 'warning')
    else:
        meal_plan.recipes.append(recipe)
        db.session.commit()
        flash("Recipe added to your meal plan!", 'success')
    print(meal_plan.recipes)
    for recipe in meal_plan.recipes:
        print(f"Recipe: {recipe}")
        print(f"Name: {getattr(recipe, 'name', 'Attribute not found')}")
        print(f"Title: {getattr(recipe, 'title', 'Attribute not found')}")
        print(f"Image URL: {getattr(recipe, 'image_url', 'Attribute not found')}")
    return redirect(url_for('api.recipe_detail', recipe_id=recipe.id,meal_plan_id=meal_plan.id))


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
