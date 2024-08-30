from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
import requests
from flask_login import login_required, current_user, login_user, logout_user
from app.models.user import User
api = Blueprint('api', __name__)

# User dahsboard
@api.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# Landing page route
@api.route('/home')
def home():
    return render_template('home.html')

@api.route('/search_recipes', methods=['GET'])
@login_required
def search_recipes():
    query = request.args.get('query')
    app_id = current_app.config['EDAMAM_APP_ID']
    api_key = current_app.config['EDAMAM_API_KEY']
    url = f"https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        recipes = response.json().get('hits', [])
        return render_template('recipe.html', recipes=recipes, query=query)
    else:
        error_message = "Failed to fetch Recipes"
        return render_template('recipe.html', error=error_message, query=query)


@api.route('/recipe_detail/<path:recipe_id>')
def recipe_detail(recipe_id):
    # app_id = current_app.config['EDAMAM_APP_ID']
    # api_key = current_app.config['EDAMAM_API_KEY']
    # url = url =f"https://api.edamam.com/api/recipes/v2?type=public&uri={recipe_id}&app_id={app_id}&app_key={api_key}"
    # response = requests.get(url)
    
    # print(response.text)
    # if response.status_code == 200:
    #     data = response.json()
    #     if data['hits']:
    #         recipe = data['hits'][0]['recipe']
    #         return render_template('recipe_detail.html', recipe=recipe)
    #     else:
    #         flash("No recipe found.", 'warning')
    # else:
    #     flash("failed to fetch recipe details.", 'danger')
    #     return redirect(url_for('api.search_recipes'))
    app_id = current_app.config['EDAMAM_APP_ID']
    api_key = current_app.config['EDAMAM_API_KEY']
    url = f"https://api.edamam.com/api/recipes/v2?type=public&uri={recipe_id}&app_id={app_id}&app_key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses

        # Debugging output
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code == 200:
            data = response.json()
            if 'hits' in data and data['hits']:
                recipe = data['hits'][0]['recipe']
                return render_template('recipe_detail.html', recipe=recipe)
            else:
                flash("No recipe found.", 'warning')
        else:
            flash(f"API Error: {response.status_code} - {response.text}", 'danger')

    except requests.exceptions.RequestException as e:
        flash(f"Request failed: {e}", 'danger')
    except ValueError as e:
        flash(f"Failed to decode JSON response: {e}", 'danger')

    return redirect(url_for('api.search_recipes'))


@api.route('/meal_plan')
@login_required
def meal_plan():
    return "welcome here you will find your meal plans"

 