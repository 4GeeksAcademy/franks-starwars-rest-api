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
from models import db, User, Favorite, Planet, Character, Vehicle

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

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets =  Planet.query.all()
    all_planets =  list(map(lambda x:x.serialize(), planets))
    return jsonify(all_planets)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet =  Planet.query.get(planet_id)
    planet = planet.serialize()
    return jsonify(planet)

@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters =  Character.query.all()
    all_characters =  list(map(lambda x:x.serialize(), characters))
    return jsonify(all_characters)

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character =  Character.query.get(character_id)
    character = character.serialize()
    return jsonify(character)

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles =  Vehicle.query.all()
    all_vehicles =  list(map(lambda x:x.serialize(), vehicles))
    return jsonify(all_vehicles)

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle =  Vehicle.query.get(vehicle_id)
    vehicle = vehicle.serialize()
    return jsonify(vehicle)

@app.route('/users', methods=['GET'])
def get_users():
    users =  User.query.all()
    all_users =  list(map(lambda x:x.serialize(), users))
    return jsonify(all_users)

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user_id = 1
    user_favorites =  Favorite.query.filter_by(user_id = current_user_id)
    user_favorites_clean =  list(map(lambda x:x.serialize(), user_favorites))
    return jsonify(user_favorites_clean)


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    current_user_id = 1
    print("planet_id from the URL", planet_id)

    favorite = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if favorite:
        return jsonify({"message": "Planet already in favorite"}), 400
    new_favorite = Favorite(user_id=current_user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite added successfuly"})

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_fav_character(character_id):
    current_user_id = 1
    print("character_id from the URL", character_id)
    
    favorite = Favorite.query.filter_by(user_id=current_user_id, character_id=character_id).first()
    if favorite:
        return jsonify({"message": "Character already in favorite"}), 400
    new_favorite = Favorite(user_id=current_user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite added successfuly"})

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_fav_vehicle(vehicle_id):
    current_user_id = 1
    print("vehicle_id from the URL", vehicle_id)
    
    favorite = Favorite.query.filter_by(user_id=current_user_id, vehicle_id=vehicle_id).first()
    if favorite:
        return jsonify({"message": "Vehicle already in favorite"}), 400
    new_favorite = Favorite(user_id=current_user_id, vehicle_id=vehicle_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite added successfuly"})

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_fav_planet(planet_id):
    current_user_id = 1
    favorite = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"message": "Planet not in favorites"}), 400
    print("Favorite to be removed", favorite)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite removed successfuly"})
    

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_fav_character(character_id):
    current_user_id = 1
    favorite = Favorite.query.filter_by(user_id=current_user_id, character_id=character_id).first()
    if not favorite:
        return jsonify({"message": "Character not in favorites"}), 400
    print("Favorite to be removed", favorite)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite removed successfuly"})

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def remove_fav_vehicle(vehicle_id):
    current_user_id = 1
    favorite = Favorite.query.filter_by(user_id=current_user_id, vehicle_id=vehicle_id).first()
    if not favorite:
        return jsonify({"message": "Vehicle not in favorites"}), 400
    print("Favorite to be removed", favorite)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message" : "Favorite removed successfuly"})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)