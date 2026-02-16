from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, PasswordField, DateField, IntegerField, SelectField, FloatField
from wtforms.validators import InputRequired, EqualTo, NumberRange

class FilterForm(FlaskForm):
    filter = RadioField("Sort By ",
        choices=["Price low to high", "Price high to low", "County A-Z"],
        default="County A-Z")
    time_filter = DateField("Select a date to see availablity from then on:  ", validators=[InputRequired()])
    submit= SubmitField("Submit")


class LoginForm(FlaskForm):
    user_id = StringField("user id: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])
    submit= SubmitField("Submit")


class RegisterForm(FlaskForm):
    user_id = StringField("user_id: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])
    password2 = PasswordField("Re-enter Password: ", validators=[InputRequired(), EqualTo("password")])
    submit= SubmitField("Submit")

class ReviewFilterForm(FlaskForm):
    filter = RadioField("Sort By ",
        choices=["Rating low to high", "Rating high to low", "Activity A-Z"],
        default="Activity A-Z")
    submit= SubmitField("Submit")

class ReviewForm(FlaskForm):
    activity_name = SelectField("This review is about ",
        choices=["Giant's Causeway", "Cliff's of Moher", "The Wild Atlantic Way",
                 "The Burren", "Titanic Experience Cobh", "Waterford Treasures Museum", 
                 "National Wax Museum", "Little Museum of Dublin", "Blarney Castle",
                 "Dublin Castle", "Ross Castle", "Kilkenny Castle",
                 "Dublin Zoo", "Nonstop Karting", "Combat Laser Tag", 
                 "We Escape Cork"])
    stars=SelectField("Please select how many stars you would give this activity", choices=["⋆", "⋆⋆", "⋆⋆⋆", "⋆⋆⋆⋆", "⋆⋆⋆⋆⋆"])
    review = StringField("Please enter your review and the activity below: ", validators=[InputRequired()])
    submit=SubmitField()

class PassChangeForm(FlaskForm):
    user_id = StringField("user id: ", validators=[InputRequired()])
    password = PasswordField("Old Password: ", validators=[InputRequired()])
    submit= SubmitField("Submit")


class PassChange2Form(FlaskForm):
    password = PasswordField("New Password: ", validators=[InputRequired()])
    password2 = PasswordField("Re-enter Password: ", validators=[InputRequired(), EqualTo("password")])
    submit= SubmitField("Submit")

class ConfirmationForm(FlaskForm):
    num_people1=IntegerField("Please input how many adults you would like to book for: ", validators=[NumberRange(1,10), InputRequired()])
    num_people2=IntegerField("Please input how many children you would like to book for: ", validators=[NumberRange(0,10), InputRequired()])
    submit=SubmitField("Click here to confirm booking")

class AdminLoginForm(FlaskForm):
    admin_id = StringField("admin id: ", validators=[InputRequired()])
    code = PasswordField("Secret Code: ", validators=[InputRequired()])
    submit= SubmitField("Submit")

class DeleteAdminForm(FlaskForm):
    activity_id = IntegerField("Enter the activity id of the activity you wish to delete: ", validators=[ InputRequired()])
    submit= SubmitField("Submit")

class AddAdminForm(FlaskForm):
    name = StringField("Name: ", validators=[InputRequired()])
    date=DateField("Date: ", validators=[InputRequired()])
    county = StringField("County: ", validators=[InputRequired()])
    category = SelectField("Category: ", choices=["Entertainment", "Nature", "Museum", "Castle"], validators=[InputRequired()])
    price = FloatField("Price: ", validators=[InputRequired(), NumberRange(0,1000)])
    pricenote = StringField("Price Note: ", validators=[InputRequired()])
    description = StringField("Description: ", validators=[InputRequired()])
    image = StringField("Image url: ", validators=[InputRequired()])
    submit= SubmitField("Submit")

class UpdateAdminForm(FlaskForm):
    activity_id=IntegerField("Please enter the id of the activity you wish to update", validators=[InputRequired(), NumberRange(0,1000)])
    attribute = SelectField("This review is about the activity's  ",
        choices=["Name", "County", "Category", "Price", "Pricenote", "Description", "Image"])
    new_value = StringField("Please enter the new value of the activity's attribute: ", validators=[InputRequired()])
    submit=SubmitField()





