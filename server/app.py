# server/app.py
#!/usr/bin/env python3

import os
from flask import Flask, make_response, abort
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# add views here
@app.route('/')
def index():
    return '<h1>Welcome to the pet directory!</h1>'


@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.get_or_404(id, description=f'Pet {id} not found')
    return f'<p>{pet.name} {pet.species}</p>'


@app.route("/species/<string:species>")
def pet_by_species(species):
    pets = Pet.query.filter_by(species=species.capitalize()).all()

    if not pets:
        abort(404, description=f'Pet species {species} not found')

    pet_names = ''.join(f'<p>{pet.name}</p>' for pet in pets)
    response_body = f'<h2>There are {len(pets)} {species}s<h2>{pet_names}'
    return response_body


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5555))
    app.run(port=port, debug=True)
