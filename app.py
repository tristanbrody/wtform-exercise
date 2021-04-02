from flask import Flask, request, redirect, render_template, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import update
from models import db, Pet, connect_db
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_agency'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['TESTING'] = True
debug = DebugToolbarExtension(app)
PLACEHOLDER_IMAGE_URL = 'https://images.unsplash.com/photo-1610337673044-720471f83677?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=966&q=80'
connect_db(app)

@app.route('/')
def show_home_page():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def show_add_pet_form():
    """Get and post requests for adding a new pet"""
    form = AddPetForm()
    if form.validate_on_submit():
        add_new_pet(form)
        flash(f'{form.data.name} successfully added!')
        return redirect(url_for('show_home_page'))
    else:
        return render_template('add_pet.html', form=form, hide_cancel_btn='')

@app.route('/pets/<pet_id_number>', methods=['GET', 'POST'])
def show_pet_details(pet_id_number):
    """Show details about a specific pet"""
    edit_pet_form = EditPetForm()
    pet = Pet.query.get(pet_id_number)
    if edit_pet_form.validate_on_submit():
        update_pet(edit_pet_form, pet)
        flash(f'{pet.name} updated successfully')
    else:
        edit_pet_form.photo_url.data = pet.photo_url
        edit_pet_form.notes.data = pet.notes
        edit_pet_form.price.data = pet.price
        edit_pet_form.available.data = pet.available
    return render_template('show_pet_details.html', pet=pet, form=edit_pet_form, hide_cancel_btn='hidden')

def add_new_pet(form):
    name = form.name.data
    species = form.species.data
    photo_url = PLACEHOLDER_IMAGE_URL if form.photo_url.data == '' else form.photo_url.data
    age = form.age.data
    notes = form.notes.data
    price = form.price.data
    new_pet = Pet(name=name,species=species,photo_url=photo_url,age=age,notes=notes,price=price)
    db.session.add(new_pet)
    db.session.commit()

def update_pet(form, pet):
    pet.photo_url = PLACEHOLDER_IMAGE_URL if pet.photo_url == '' else form.photo_url.data
    pet.notes = form.notes.data
    pet.price = form.price.data
    pet.available = form.available.data
    db.session.add(pet)
    db.session.commit()