from app import myapp_obj
from flask import render_template, redirect, request, flash
from app.forms import LoginForm, RecipeForm, CreateAccountForm
from app.models import User, Recipe
from app import db
from flask_login import current_user, login_required, login_user, logout_user

# Main route, renders home page and displays all recipes
@myapp_obj.route("/")
def main():
    recipes = Recipe.query.all()  # Fetch all recipes from the database
    return render_template("home.html", title="Home Page", recipes=recipes)  # Render home.html and pass recipes to the template

# Route for creating a new user account
@myapp_obj.route("/create_account", methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm()  # Create form for user to create an account
    if form.validate_on_submit():  # Validate the form when the user submits it
        # Create a new user and hash their password
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)  # Add the user to the session
        db.session.commit()  # Commit the changes to the database
        return redirect("/")  # Redirect to the homepage after account creation
    return render_template("create_account.html", title="Create Account", form=form)  # Render create_account.html and pass the form

# Route for logging in the user
@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create form for user to log in
    if current_user.is_authenticated:  # If the user is already logged in
        return redirect('/recipes')  # Redirect to the recipes page

    if request.method == 'POST':  # If the form is submitted
        user = User.query.filter_by(username=form.username.data).first()  # Query for the user by username
        if user is not None and user.check_password(password=form.password.data):  # Check if the password is correct
            login_user(user)  # Log the user in
            return redirect("/recipes")  # Redirect to the recipes page
        else:
            flash("Invalid username or password", "danger")  # Show an error message if login fails
    return render_template("login.html", form=form)  # Render login.html and pass the form

# Route for displaying the user's own recipes
@myapp_obj.route("/recipes")
@login_required  # Ensure the user is logged in before accessing this route
def recipe():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()  # Fetch recipes only created by the logged-in user
    return render_template("recipes.html", title="Recipes", recipes=recipes)  # Render recipes.html and pass the recipes

# Route for adding a new recipe
@myapp_obj.route("/recipe/new", methods=["POST", "GET"])
@login_required  # Ensure the user is logged in before accessing this route
def add_recipe():
    form = RecipeForm()  # Create a new form instance for adding a recipe
    if form.validate_on_submit():  # Validate the form when the user submits it
        # Create a new recipe and associate it with the current user
        new_recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            user_id=current_user.id
        )
        db.session.add(new_recipe)  # Add the new recipe to the session
        db.session.commit()  # Commit the changes to the database
        return redirect("/recipes")  # Redirect to the recipes page
    return render_template("add_recipe.html", title="Add New Recipe", form=form)  # Render add_recipe.html and pass the form

# Route for displaying a specific recipe
@myapp_obj.route("/recipe/<int:num>", methods=['GET'])
@login_required  # Ensure the user is logged in before accessing this route
def retrieve_recipe(num):
    recipe = Recipe.query.get(num)  # Fetch the recipe by its ID
    if recipe is None:  # If the recipe does not exist
        flash("Recipe not found.", "danger")  # Show a flash message
        return redirect("/recipes")  # Redirect to the recipes page
    # Format the ingredients and instructions
    formatted_ingredients = recipe.format_ingredients(recipe.ingredients)
    formatted_instructions = recipe.format_instructions(recipe.instructions)
    return render_template("show_recipe.html", title=recipe.title, recipe=recipe, 
                           ingredients=formatted_ingredients, instructions=formatted_instructions)  # Render show_recipe.html with the recipe data

# Route for deleting a specific recipe
@myapp_obj.route("/recipe/<int:num>/delete", methods=["POST", "GET"])
@login_required  # Ensure the user is logged in before accessing this route
def delete_recipe(num):
    recipe_to_delete = Recipe.query.get(num)  # Fetch the recipe by its ID
    if recipe_to_delete and recipe_to_delete.user_id == current_user.id:  # Check if the user is the owner of the recipe
        db.session.delete(recipe_to_delete)  # Delete the recipe from the session
        db.session.commit()  # Commit the changes to the database
        flash("Recipe deleted successfully!", "success")  # Show a success message
    else:
        flash("You are not authorized to delete this recipe.", "danger")  # Show an error message if the user is not the owner
    return redirect("/recipes")  # Redirect to the recipes page

# Route for logging out the user
@myapp_obj.route('/logout')
def logout():
    logout_user()  # Log the user out
    return redirect('/')  # Redirect to the homepage