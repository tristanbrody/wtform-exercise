from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Regexp, URL, NumberRange, Optional

class AddPetForm(FlaskForm):
    """Form for adding a new pet"""

    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField("Species", validators=[InputRequired(), Regexp('([cC]at|[dD]og|[pP]orcupine)', message="Accepted species are cat, dog or porcupine")])
    photo_url = StringField("Add a link to a photo of your pet", validators=[Optional(), URL(message="Please enter a valid URL")])
    age = IntegerField("Your pet's age in years", validators=[InputRequired(), NumberRange(min=0,max=30, message="Age must be between 0-30 (inclusive)")])
    price = FloatField("Price in USD", validators=[InputRequired()])
    notes = StringField("Anything special we should know")

class EditPetForm(FlaskForm):
    """Form with limited fields for editing an existing pet"""

    photo_url = StringField("Add a link to a photo of your pet", validators=[Optional(), URL(message="Please enter a valid URL")])
    price = FloatField("Price in USD", validators=[InputRequired()])
    notes = StringField("Anything special we should know")
    available = BooleanField()
