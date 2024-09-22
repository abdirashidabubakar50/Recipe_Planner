import requests
import pandas as pd
from os.path import exists
import json
import time

API_KEY = os.getenv('SPOONACULAR_API_KEY')
BASE_URL_RECIPES = 'https://api.spoonacular.com/recipes/random'
BATCH_SIZE = 10  # Fetch 10 recipes per batch to manage rate limits better
TARGET_NEW_RECIPES = 100  # Target number of new recipes per request
csv_filename = 'recipes.csv'
ids_filename = 'fetched_ids.txt'
csv_columns = ['id', 'name', 'ingredients', 'instructions', 'diet_type', 'allergies', 'image_url', 'nutrients']


def fetch_recipes(batch_size=BATCH_SIZE):
    """Fetch a batch of random recipes from the Spoonacular API."""
    params = {'number': batch_size, 'apiKey': API_KEY}
    response = requests.get(BASE_URL_RECIPES, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"API Response: {json.dumps(data, indent=2)}")  # Print the raw response for inspection
        return data.get('recipes', [])
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return []


def parse_recipe_data(recipe):
    """Parse the recipe data and return a dictionary of parsed data."""
    try:
        instructions = ' | '.join(
            [step['step'] for step in recipe.get('analyzedInstructions', [])[0].get('steps', [])]
        ) if recipe.get('analyzedInstructions') else ''
        ingredients = recipe.get('extendedIngredients', [])
        ingredients_json = json.dumps(ingredients)

        parsed_recipe = {
            'id': recipe['id'],
            'name': recipe['title'],
            'ingredients': ingredients_json,
            'instructions': instructions,
            'diet_type': ', '.join(recipe.get('diets', [])),
            'image_url': recipe.get('image', ''),
            'nutrients': json.dumps(recipe.get('nutrition', {}).get('nutrients', [])) 
        }

        print(f"Parsed Recipe: {parsed_recipe}")
        return parsed_recipe
    except Exception as e:
        print(f"Error parsing recipe: {e}")
        return None


def load_existing_recipes(filename):
    """Load existing recipes from a CSV file."""
    if exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=csv_columns)


def load_fetched_ids(filename):
    """Load already fetched recipe IDs from a file."""
    if exists(filename):
        with open(filename, 'r') as file:
            return set(line.strip() for line in file)
    else:
        return set()


def save_fetched_ids(fetched_ids, filename):
    """Save fetched recipe IDs to a file."""
    with open(filename, 'w') as file:
        for recipe_id in fetched_ids:
            file.write(f"{recipe_id}\n")


def fetch_and_save_to_csv(filename=csv_filename, ids_filename=ids_filename, target_new_recipes=TARGET_NEW_RECIPES):
    """Fetch recipes from the API and save new ones to a CSV file."""
    all_recipes = []
    existing_recipes = load_existing_recipes(filename)
    existing_ids = set(existing_recipes['id'].astype(str))
    fetched_ids = load_fetched_ids(ids_filename)

    while len(all_recipes) < target_new_recipes:
        recipes = fetch_recipes()
        print(f"Fetched {len(recipes)} recipes from API")  # Debug fetched count
        if not recipes:
            print("No recipes fetched, breaking the loop.")
            break  # Stop if there are no recipes fetched or an error occurred

        for recipe in recipes:
            recipe_id = str(recipe['id'])
            if recipe_id not in existing_ids and recipe_id not in fetched_ids:
                parsed_recipe = parse_recipe_data(recipe)
                if parsed_recipe:  # Check if parsing was successful
                    all_recipes.append(parsed_recipe)
                    existing_ids.add(recipe_id)
                    fetched_ids.add(recipe_id)
                    print(f"Fetched new recipe: {recipe['title']}")

        print(f"Current count of new recipes: {len(all_recipes)}")

        # Add delay to avoid hitting API rate limits
        if len(all_recipes) < target_new_recipes:
            time.sleep(1)  # Adjust delay as necessary to manage rate limits

        # Check if we are hitting the rate limit
        if len(recipes) < BATCH_SIZE:
            print("Potential rate limit hit or no more unique recipes available. Stopping.")
            break

    if all_recipes:
        df_new_recipes = pd.DataFrame(all_recipes, columns=csv_columns)
        df_existing_recipes = pd.concat([existing_recipes, df_new_recipes], ignore_index=True)
        df_existing_recipes.to_csv(filename, index=False)
        save_fetched_ids(fetched_ids, ids_filename)
        print(f"Saved {len(all_recipes)} new recipes to {filename}")
    else:
        print("No new recipes to add.")


if __name__ == "__main__":
    fetch_and_save_to_csv()
