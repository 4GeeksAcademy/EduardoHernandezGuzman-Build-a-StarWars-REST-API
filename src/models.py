from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(250), nullable=False)
    height = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)

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

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)  

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