from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators, EmailField, TextAreaField

# Login form for user authentication
class LoginForm(FlaskForm):
    username = StringField('USERNAME', validators=[validators.DataRequired()])  # Username field, requires data
    password = PasswordField('Password', validators=[validators.Length(min=4, max=35)])  # Password field with a length constraint
    submit = SubmitField("Sign in")  # Submit button with the label "Sign in"
    remember_me = BooleanField("Remember Me")  # Checkbox for "Remember Me" functionality

# Form for creating a new account
class CreateAccountForm(FlaskForm):
    username = StringField('USERNAME', validators=[validators.DataRequired()])  # Username field, requires data
    password = PasswordField('Password', validators=[validators.Length(min=4, max=35)])  # Password field with length constraint
    email = EmailField('Email', validators=[validators.DataRequired()])  # Email field, requires data
    submit = SubmitField("Create Account")  # Submit button with the label "Create Account"

# Form for adding a new recipe
class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[validators.DataRequired()])  # Recipe title field, requires data
    description = TextAreaField('Description', validators=[validators.DataRequired()])  # Recipe description, requires data
    ingredients = TextAreaField('Ingredients', validators=[validators.DataRequired()])  # Ingredients field, requires data
    instructions = TextAreaField('Instructions', validators=[validators.DataRequired()])  # Instructions field, requires data
    submit = SubmitField("Add Recipe")  # Submit button with the label "Add Recipe"
