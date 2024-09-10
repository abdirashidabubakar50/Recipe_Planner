import pandas as pd
import json
from app import create_app, db
from app.models.all_recipes import AllRecipe

app = create_app()

def clean_value(value, default=None):
    """Utility function to clean values, converting NaN to a default."""
    if pd.isna(value):
        return default
    return value

def format_ingredients(ingredients_json):
    """
    Convert JSON string of ingredients into a readable format.
    Example output: "2 cups flour, 1 tsp salt, 200ml milk"
    """
    try:
        ingredients = json.loads(ingredients_json)  # Parse the JSON string
        formatted_ingredients = []
        for ingredient in ingredients:
            # Extract name, amount, and unit
            amount = ingredient.get('amount', '')
            unit = ingredient.get('unit', '')
            name = ingredient.get('name', '')
            # Format into a readable string
            formatted_ingredient = f"{amount} {unit} {name}".strip()
            formatted_ingredients.append(formatted_ingredient)
        return ', '.join(formatted_ingredients)  # Join all ingredients into a single string
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return ingredients_json  # Fallback to raw JSON string if parsing fails

def format_nutrients(nutrients_json):
    """
    Convert JSON string of nutrients into a readable format.
    Example output: "Calories: 200 kcal, Protein: 10 g, Fat: 5 g"
    """
    try:
        nutrients = json.loads(nutrients_json)  # Parse the JSON string
        formatted_nutrients = []
        for nutrient in nutrients:
            # Extract name, amount, and unit
            name = nutrient.get('name', '')
            amount = nutrient.get('amount', '')
            unit = nutrient.get('unit', '')
            # Format into a readable string
            formatted_nutrient = f"{name}: {amount} {unit}".strip()
            formatted_nutrients.append(formatted_nutrient)
        return ', '.join(formatted_nutrients)  # Join all nutrients into a single string
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return nutrients_json  # Fallback to raw JSON string if parsing fails

def save_recipe(row):
    """Save a recipe from the DataFrame row to the database."""
    with app.app_context():
        try:
            # Check if a recipe with the same ID already exists
            existing_recipe = AllRecipe.query.get(row['id'])
            if existing_recipe:
                print(f"Recipe with ID {row['id']} already exists. Skipping.")
                return
            
            # Handle missing or NaN values
            allergies = clean_value(row.get('allergies', []), [])
            image_url = clean_value(row.get('image_url', ''), '')
            diet_type = clean_value(row.get('diet_type', ''), '')

            # Truncate diet_type if it exceeds 150 characters
            if len(diet_type) > 150:
                diet_type = diet_type[:150]
                print(f"Truncated diet_type to 150 characters: {diet_type}")

            # Format ingredients from JSON to readable format
            formatted_ingredients = format_ingredients(row['ingredients'])
            
            # Format nutrients from JSON to readable format
            formatted_nutrients = format_nutrients(row.get('nutrients', '[]'))

            # Convert allergies to JSON string
            allergies_json = json.dumps(allergies)

            # Check the types of fields to ensure correct parsing
            print(f"Name: {row['name']}, Ingredients: {formatted_ingredients}, Instructions: {row['instructions']}, Allergies: {allergies_json}, Image URL: {image_url}, Nutrients: {formatted_nutrients}")

            recipe = AllRecipe(
                id=row['id'],
                name=row['name'],
                ingredients=formatted_ingredients,  # Use formatted ingredients here
                instructions=row['instructions'],
                diet_type=diet_type,
                allergies=allergies_json,
                image_url=image_url,
                nutrients=formatted_nutrients  # Save formatted nutrients here
            )
            recipe.save()
            print(f"Saved recipe: {recipe.name}")
        except Exception as e:
            print(f"Error saving recipe: {e}")
            db.session.rollback()

def import_recipes_from_csv(filename='recipes.csv'):
    """Import recipes from a CSV file and save them to the database."""
    with app.app_context():
        df = pd.read_csv(filename)
        # Fill NaN values globally before processing
        df.fillna({'diet_type': '', 'allergies': '[]', 'image_url': '', 'nutrients': '[]'}, inplace=True)
        print(f"CSV Columns: {df.columns.tolist()}")  # Debugging: print column names
        print(df.head())  # Check the first few rows to verify data
        df.apply(save_recipe, axis=1)

if __name__ == "__main__":
    import_recipes_from_csv()
