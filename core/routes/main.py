from flask import Blueprint, jsonify, request
from ..models import Wine, Notes

from ..extensions import db

main = Blueprint('main', __name__)

# index
@main.route('/', methods=['GET'])
def index():
    return '''
<h1>Wines API</h1>
<p><a href="http://127.0.0.1:5000/wines/">GET all wines</a></p>
<p><a href="http://127.0.0.1:5000/wines/1">GET One wine</a></p>
'''


# GET
@main.route('/wines/', methods=['GET'])
def get_all_wines():
    return jsonify([wine.to_dict() for wine in Wine.query.all()])


@main.route('/wines/<int:wine_id>/', methods=['GET'])
def get_one_wine(wine_id):
    wine = Wine.query.get(wine_id)

    if not wine:
        return jsonify({
            'error': 'Wine not found',
            'code': 404
        }), 404

    return jsonify(wine.to_dict())


# POST
@main.route('/wines/add/', methods=['POST'])
def add_wine():
    if request.method == 'POST':
        name = request.form.get('name')
        color = request.form.get('color')
        notes = request.form.get('notes')
        country = request.form.get('country')
        region = request.form.get('region')
        grape = request.form.get('grape')
        abv = request.form.get('abv')

        print('name: ', name)
        print('color: ', color)
        print('notes: ', notes)
        print('country: ', country)
        print('region: ', region)
        print('grape: ', grape)
        print('abv: ', abv) 


        new_wine = Wine(
            name=name,
            color=color,
            notes=notes,
            country=country,
            region=region,
            grape=grape,
            abv=float(abv)
        )

        print(new_wine)

        db.session.add(new_wine)
        db.session.commit()

        all_wines = Wine.query.all()

        for note in notes.split(', '):
            note_exists = bool(Notes.query.filter_by(name=note).first())
            if not note_exists:
                new_note = Notes(
                    name=note
                )
                db.session.add(new_note)
                db.session.commit()
        
        return 'Wine Added'


# update
@main.route('/wines/<int:wine_id>/edit/', methods=['POST'])
def edit_wine(wine_id):
    if request.method == 'POST':
        name = request.form.get('name')
        color = request.form.get('color')
        notes = request.form.get('notes')
        country = request.form.get('country')
        region = request.form.get('region')
        grape = request.form.get('grape')
        abv = request.form.get('abv')

        wine = Wine.query.get(wine_id)

        wine.name = name
        wine.color = color
        wine.notes = notes
        wine.country = country
        wine.region = region
        wine.grape = grape
        wine.abv = abv

        db.session.commit()

        return f"Wine {wine} edited"
    

# delete
@main.route('/wines/<int:wine_id>/delete/', methods=['GET', 'DELETE'])
def remove_wine(wine_id):
    wine = Wine.query.get(wine_id)
    db.session.delete(wine)
    db.session.commit()

