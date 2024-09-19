
# Smart Recipe Planner

## Project Overview
The **Smart Recipe Planner** is a web application designed to help users plan their meals, find personalized recipes based on dietary preferences, and generate shopping lists. It allows users to organize meals using a calendar and schedule recipes for different days.

## Features
- **User Registration & Profile Setup**: Users can sign up, log in, and set dietary preferences.
- **Recipe Search**: Search for recipes by ingredients, meal types, or dietary restrictions.
- **Meal Planning**: Create meal plans for specific dates and organize meals for the week.
- **Grocery List Generation**: Automatically generate a grocery list based on selected recipes.
- **Unscheduled Recipes & Calendar Integration**: Manage unscheduled recipes and easily add them to a meal plan using the FullCalendar API.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/recipe-planner.git
   ```
2. Navigate to the project directory:
   ```bash
   cd recipe-planner
   ```
3. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # for Linux/macOS
   venv\Scriptsctivate  # for Windows
   pip install -r requirements.txt
   ```
4. Set up the MySQL database and apply migrations:
   ```bash
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

## Usage
- Create an account or log in.
- Set up your dietary preferences (e.g., vegetarian, gluten-free).
- Search for recipes using keywords or ingredients.
- Add recipes to your meal plan for specific days.
- View your meal plan in the calendar and generate a grocery list.

## Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (FullCalendar API integration)
- **Database**: MySQL
- **Deployment**: Render.com

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes and push to your branch.
4. Open a pull request.

## License
This project is licensed under the MIT License.
