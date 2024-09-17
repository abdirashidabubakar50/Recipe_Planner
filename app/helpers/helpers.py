from app.models.all_recipes import AllRecipe
from sqlalchemy import or_, func, cast, String
from flask_login import current_user
from app import db


def get_recipes(db, user=current_user, keyword=None, limit=1000):
    """
    Retrieve recipes from the database based on user preferences, search keywords or
    randomly.

    Args:
         db_sesion (Session): SQLAlchemy session to interact with the database
         user (User, optiononal): the current user object to filter by their preference
         keyword (str, optional): Search keyword to filter the recipes  by name or ingredient
         limit( int, optional): Number of recipes to return, default is 20

    
    Returns:
        list: A list of Recipe objects.
    
    """
 
    query = db.session.query(AllRecipe)

    """
    Filter by user preference if provided

    """
    if user.preferences:
        preferences = user.preferences
        preferences = [pref.lower() for pref in user.preferences]
        query = query.filter(or_(*[AllRecipe.diet_type.ilike(f'%{pref}%') for p in preferences]))
    
    """
    filter by search keyword if provided
    """
    if keyword:
        print(f"Filtering recipes by name with keyword: {keyword}")
        query = query.filter(
            AllRecipe.name.ilike(f'%{keyword}%') | 
            cast(AllRecipe.ingredients, String).ilike(f'%{keyword}%')
        )
    
    """
    if no preferences or keyword(searches), select random recipes
    """
    if not(user and user.preferences) and not keyword:
        print("Fetching random recipes as no preferences or keywords are provided.")
        query = query.order_by(func.random())
    
    # Limit the number of recipes returned
    recipes = query.limit(limit).all()

    return recipes