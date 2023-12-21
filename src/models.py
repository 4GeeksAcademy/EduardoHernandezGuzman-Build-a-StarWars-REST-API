from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



############################# USUARIOS ###################################
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    #Relación con character_fav y planet_fav
    character_fav = db.relationship("Character_fav", back_populates="user")
    planet_fav = db.relationship("Planet_fav", back_populates="user")


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

############################# PERSONAJES ################################### 
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(250), nullable=False)
    height = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)

    #Relación con character_fav
    character_fav = db.relationship("Character_fav", back_populates="character")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
        }

class Character_fav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    user = db.relationship("User", back_populates="character_fav")
    character = db.relationship("Character", back_populates="character_fav")

    def __repr__(self):
        return '<Character_fav %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "user_id": self.user_id,
        }


############################# PLANETAS ###################################
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)  

    #Relación con planet_fav
    planet_fav = db.relationship("Planet_fav", back_populates="planet")

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
        }

class Planet_fav(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    user = db.relationship("User", back_populates="planet_fav")
    planet = db.relationship("Planet", back_populates="planet_fav")

    def __repr__(self):
        return '<Planet_fav %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id,
        }
