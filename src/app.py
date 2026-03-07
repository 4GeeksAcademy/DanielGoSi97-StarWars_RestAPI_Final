"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta, Nave, Favorites_Personaje, Favorites_Planeta, Favorites_Nave
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    all_users = User.query.all()
    results = list(map(lambda user: user.serialize(),all_users))

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users": results
    }

    return jsonify(response_body), 200

@app.route('/test', methods=['GET'])
def test():

    response_body = {
        "msg": "Hello, this is your GET /test response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():

    people = Personaje.query.all()
    results = list(map(lambda person: person.serialize(), people))

    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):

    person = Personaje.query.get(people_id)

    if person is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404

    return jsonify(person.serialize()), 200


@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    results = list(map(lambda user: user.serialize(), users))

    return jsonify(results), 200


@app.route('/users/favorites', methods=['GET'])
def get_favorites():

    user_id = 1

    fav_people = Favorites_Personaje.query.filter_by(user_id=user_id).all()
    fav_planets = Favorites_Planeta.query.filter_by(user_id=user_id).all()

    response = {
        "favorite_people": [fav.serialize() for fav in fav_people],
        "favorite_planets": [fav.serialize() for fav in fav_planets]
    }

    return jsonify(response), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):

    user_id = 1

    new_favorite = Favorites_Planeta(
        user_id=user_id,
        planeta_id=planet_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Planet added to favorites"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):

    user_id = 1

    new_favorite = Favorites_Personaje(
        user_id=user_id,
        personaje_id=people_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "People added to favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):

    user_id = 1

    favorite = Favorites_Planeta.query.filter_by(
        user_id=user_id,
        planeta_id=planet_id
    ).first()

    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):

    user_id = 1

    favorite = Favorites_Personaje.query.filter_by(
        user_id=user_id,
        personaje_id=people_id
    ).first()

    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)