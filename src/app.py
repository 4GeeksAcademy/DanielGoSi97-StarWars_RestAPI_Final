import os
import sys
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

# Forzamos la ruta interna para Render
sys.path.append(os.path.dirname(__file__))

from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta, Nave, Favorites_Personaje, Favorites_Planeta, Favorites_Nave

app = Flask(__name__)

# Configuración de DB para Render (Cambia postgres:// por postgresql://)
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

db.init_app(app)

# CREAR TABLAS (Si no haces esto, la app falla al no encontrar tablas)
with app.app_context():
    db.create_all()

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
    fav_ships = Favorites_Nave.query.filter_by(user_id=user_id).all() # <-- Faltaba esta

    response = {
        "favorite_people": [fav.serialize() for fav in fav_people],
        "favorite_planets": [fav.serialize() for fav in fav_planets],
        "favorite_starships": [fav.serialize() for fav in fav_ships]
    }

    return jsonify(response), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # Hacemos test ya que no hay definición de usuario en el ejercicio
    user_id = 1

    new_favorite = Favorites_Planeta(
        user_id=user_id,
        planeta_id=planet_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Planet added to favorites"}), 201

#Reemplazo de admin por endpoints

@app.route('/people', methods=['POST'])
def create_person():
    body = request.get_json()
    if body is None:
        return jsonify({"msg": "Cuerpo no puede estar vacio"}), 400
    if "nombre" not in body:
        return jsonify({"msg": "Nombre es obligatorios"}), 400

    new_person = Personaje(
        nombre=body['nombre'],
        id_planeta=body.get('id_planeta'),
        id_nave=body.get('id_nave') 
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify({"msg": "Personaje creado", "result": new_person.serialize()}), 201

@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.get_json()
    if body is None or "nombre" not in body or "clima" not in body:
        return jsonify({"msg": "Nombre y clima son obligatorios"}), 400

    new_planet = Planeta(
        nombre=body['nombre'],
        clima=body['clima']
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg": "Planeta creado", "result": new_planet.serialize()}), 201

@app.route('/starships', methods=['POST'])
def create_starship():
    body = request.get_json()
    if body is None or "nombre" not in body or "modelo" not in body:
        return jsonify({"msg": "Nombre y modelo son obligatorios"}), 400

    new_ship = Nave(
        nombre=body['nombre'],
        modelo=body['modelo']
    )
    db.session.add(new_ship)
    db.session.commit()
    return jsonify({"msg": "Nave creada", "result": new_ship.serialize()}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    # Hacemos test ya que no hay definición de usuario en el ejercicio
    user_id = 1

    new_favorite = Favorites_Personaje(
        user_id = user_id,
        personaje_id = people_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "People added to favorites"}), 201

    #crear planeta crear personaje crear nave

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Hacemos test ya que no hay definición de usuario en el ejercicio
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
    # Hacemos test ya que no hay definición de usuario en el ejercicio
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

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planeta.query.all()
    return jsonify(list(map(lambda planet: planet.serialize(), planets))), 200

@app.route('/starships', methods=['GET'])
def get_starships():
    ships = Nave.query.all()
    return jsonify(list(map(lambda nave: nave.serialize(), ships))), 200

@app.route('/favorite/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(starship_id):
    user_id = 1
    new_favorite = Favorites_Nave(user_id=user_id, nave_id=starship_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Starship added to favorites"}), 201

@app.route('/favorite/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(starship_id):
    user_id = 1
    favorite = Favorites_Nave.query.filter_by(user_id=user_id, nave_id=starship_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)