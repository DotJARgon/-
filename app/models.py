from app import db
import enum

class Hand(enum.Enum):
    L = 1
    R = 2
    B = 3
    N = 4
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return self.username

class People(db.Model):
    playerid = db.Column(db.String(100), primary_key=True, nullable=False)
    
    birthYear = db.Column(db.Integer())
    birthMonth = db.Column(db.Integer())
    birthDay = db.Column(db.Integer())
    birthCountry = db.Column(db.String(100))
    birthState = db.Column(db.String(100))
    birthCity = db.Column(db.String(100))

    deathYear = db.Column(db.Integer())
    deathMonth = db.Column(db.Integer())
    deathDay = db.Column(db.Integer())
    deathCountry = db.Column(db.String(100))
    deathState = db.Column(db.String(100))
    deathCity = db.Column(db.String(100))

    debutYear = db.Column(db.Integer())
    debutMonth = db.Column(db.Integer())
    debutDay = db.Column(db.Integer())
    debutCountry = db.Column(db.String(100))
    debutState = db.Column(db.String(100))
    debutCity = db.Column(db.String(100))

    finalGameYear = db.Column(db.Integer())
    finalGameMonth = db.Column(db.Integer())
    finalGameDay = db.Column(db.Integer())
    finalGameCountry = db.Column(db.String(100))
    finalGameState = db.Column(db.String(100))
    finalGameCity = db.Column(db.String(100))

    name = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float())
    height = db.Column(db.Float())
    batHand = db.Column(db.Enum(Hand), default=Hand.N)
    throwHand = db.Column(db.Enum(Hand), default=Hand.N)

class Parks(db.Model):
    parkId = db.Column(db.String(32), primary_key=True, nullable=False)
    parkName = db.Column(db.String(100), nullable=False)
    parkAlias = db.Column(db.String(100))
    parkCountry = db.Column(db.String(100), nullable=False)
    parkState = db.Column(db.String(100), nullable=False)
    parkCity = db.Column(db.String(100), nullable=False)

