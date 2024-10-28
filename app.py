from flask import Flask, render_template, redirect, flash, request
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Connect the database and initialize the debug toolbar
connect_db(app)
toolbar = DebugToolbarExtension(app)

@app.route('/')
def list_pets():
    """Show a list of all available pets."""
    pets = Pet.query.all()  # Query all pets from the database
    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def show_add_form():
    """Show a form to add a new pet and handle submission."""
    form = AddPetForm()

    if form.validate_on_submit():  # If the form is valid, add the new pet
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data or None,
            age=form.age.data or None,
            notes=form.notes.data or None,
            available=True  # Default the pet to be available
        )

        # Add the pet to the database and commit the changes
        db.session.add(new_pet)
        db.session.commit()

        flash(f"Added {new_pet.name} the {new_pet.species}!", "success")
        return redirect('/')

    # If form is not valid or it's a GET request, render the form again
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_edit_form(pet_id):
    """Show a form to edit pet details and handle form submission."""
    pet = Pet.query.get_or_404(pet_id)  # Get the pet by ID or 404 if not found
    form = EditPetForm(obj=pet)  # Populate the form with the pet's existing data

    if form.validate_on_submit():  # If the form is valid, update the pet's info
        pet.photo_url = form.photo_url.data or None
        pet.notes = form.notes.data or None
        pet.available = form.available.data

        # Commit the changes to the database
        db.session.commit()
        flash(f"Updated {pet.name}'s information.", "success")
        return redirect(f'/{pet_id}')

    # If it's a GET request or form validation fails, show the form again
    return render_template('pet_detail.html', pet=pet, form=form)

if __name__ == '__main__':
    app.run(debug=True)




