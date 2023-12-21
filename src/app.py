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
from models import db, User , Character, Planet , Character_fav , Planet_fav
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



############################# METODO GET ###################################

#Traer a los User
@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    resultados = list(map(lambda item: item.serialize(), users))
    
    if not users:
        return jsonify(message="No se han encontrado users"), 404

    return jsonify(resultados), 200

#Traer a un usuario concreto
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user2(user_id):
    user = User.query.get(user_id)  

    if user is None:
        return jsonify(message="Usuario no encontrado"), 404

    return jsonify(user.serialize()), 200

#Traer a los favoritos de un usuario
@app.route('/user/favorites', methods=['GET'])
def get_user_fav():
    
    users = User.query.all()
    
    user_favorites = []
    
    for user in users:
        user_favorites.append({
            "user_id": user.id,
            "username": user.username,
            "character_favorites": [character_fav.character.serialize() for character_fav in user.character_fav],
            "planet_favorites": [planet_fav.planet.serialize() for planet_fav in user.planet_fav]
        })
    
    return jsonify(user_favorites), 200



#Traer a los Character
@app.route('/character', methods=['GET'])
def get_character():
    characters = Character.query.all() 
    resultados = list(map(lambda item: item.serialize(), characters))
    
    if not characters:
        return jsonify(message="No se han encontrado character"), 404

    return jsonify(resultados), 200

#Traer a un character concreto
@app.route('/character/<int:character_id>', methods=['GET'])
def get_character2(character_id):
    character = Character.query.get(character_id)  

    if character is None:
        return jsonify(message="Personaje no encontrado"), 404

    return jsonify(character.serialize()), 200

#Traer a los Character_fav
@app.route('/character_fav', methods=['GET'])
def get_character_fav():
    characters_fav = Character_fav.query.all() 
    resultados = list(map(lambda item: item.serialize(), characters_fav))
    
    if not characters_fav:
        return jsonify(message="No se han encontrado character"), 404

    return jsonify(resultados), 200



#Traer a los Planet
@app.route('/planet', methods=['GET'])
def get_planet():
    planets = Planet.query.all() 
    resultados = list(map(lambda item: item.serialize(), planets))
    
    if not planets:
        return jsonify(message="No se han encontrado planets"), 404

    return jsonify(resultados), 200

#Traer a un planet concreto
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet2(planet_id):
    planet = Planet.query.get(planet_id)  

    if planet is None:
        return jsonify(message="Planeta no encontrado"), 404

    return jsonify(planet.serialize()), 200

#Traer a los Planet_fav
@app.route('/planet_fav', methods=['GET'])
def get_planet_fav():
    planets_fav = Planet_fav.query.all() 
    resultados = list(map(lambda item: item.serialize(), planets_fav))
    
    if not planets_fav:
        return jsonify(message="No se han encontrado planet"), 404

    return jsonify(resultados), 200



############################# METODO POST ###################################

#Crear nuevo User 
@app.route('/user', methods=['POST'])
def add_new_user():
    request_body_user = request.get_json()

   
    if (
        "email" not in request_body_user
        or "password" not in request_body_user
        or "username" not in request_body_user
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    new_user = User(
        username=request_body_user["username"],
        email=request_body_user["email"],
        password=request_body_user["password"],
        is_active=request_body_user["is_active"]
    )

    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "msg": "Nuevo user añadido exitosamente"
    }

    return jsonify(response_body), 200


#Crear nuevo Character
@app.route('/character', methods=['POST'])
def add_new_character():
    body = request.get_json()
    # Verificar si los datos esperados están presentes para el personaje
    if (
        "name" not in body
        or "height" not in body
        or "mass" not in body
        or "hair_color" not in body
        or "skin_color" not in body
    ):
        return jsonify({"error": "Datos incompletos"}), 400
    # Crear el personaje con los datos recibidos
    new_character = Character(
        name=body["name"],
        height=body["height"],
        mass=body["mass"],
        hair_color=body["hair_color"],
        skin_color=body["skin_color"]
    )
    # Agregar y confirmar los cambios en la base de datos
    db.session.add(new_character)
    db.session.commit()

    response_body = {
        "msg": "Nuevo character añadido exitosamente"
    }

    return jsonify(response_body), 200

#Crear nuevo character_fav
@app.route('/character_fav', methods=['POST'])
def add_new_character_fav():
    request_body_fav_character = request.get_json()


    if (
        "character_id" not in request_body_fav_character
        or "user_id" not in request_body_fav_character
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    
    new_fav_character = Character_fav(
        character_id=request_body_fav_character["character_id"],
        user_id=request_body_fav_character["user_id"]
    )
    
   
    db.session.add(new_fav_character)
    db.session.commit()

    response_body = {
        "msg": "Nuevo character_fav añadido exitosamente"
    }

    return jsonify(response_body), 200




#Crear nuevo Planet
@app.route('/planet', methods=['POST'])
def add_new_planet():
    body = request.get_json()
    
    if (
        "name" not in body
        or "population" not in body
        or "terrain" not in body
        or "climate" not in body
    ):
        return jsonify({"error": "Datos incompletos"}), 400
   
    new_planet = Planet(
        name=body["name"],
        population=body["population"],
        terrain=body["terrain"],
        climate=body["climate"]
    )
    
    db.session.add(new_planet)
    db.session.commit()

    response_body = {
        "msg": "Nuevo planet añadido exitosamente"
    }

    return jsonify(response_body), 200


#Crear nuevo planet_fav
@app.route('/planet_fav', methods=['POST'])
def add_new_planet_fav():
    request_body_fav_planet = request.get_json()


    if (
        "planet_id" not in request_body_fav_planet
        or "user_id" not in request_body_fav_planet
    ):
        return jsonify({"error": "Datos incompletos"}), 400

    
    new_fav_planet = Planet_fav(
        planet_id=request_body_fav_planet["planet_id"],
        user_id=request_body_fav_planet["user_id"]
    )
    
   
    db.session.add(new_fav_planet)
    db.session.commit()

    response_body = {
        "msg": "Nuevo planet_fav añadido exitosamente"
    }

    return jsonify(response_body), 200



############################# METODO DELETE ###################################




#Aquí el código






















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
