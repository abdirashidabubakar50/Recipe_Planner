from flask import Blueprint, render_template, request, current_app
import requests

api = Blueprint('api', __name__)

# User dahsboard
@api.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')


# Landing page route
@api.route('/home')
def home():
    return render_template('home.html')

@api.route('/search_recipes', methods=['GET'])
def recipes():
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

@api.route('/meal_plan')
def meal_plan():
    return "welcome here you will find your meal plans"

 