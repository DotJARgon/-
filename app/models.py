from app import db
import enum
class Division(enum.Enum):
    W = 1 # west
    E = 2 # east
    C = 3 # central
    NONE = 4 # no division
class YNChoice(enum.Enum):
    Y = 1
    N = 2
    NA = 3
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
    playerId = db.Column(db.String(100), primary_key=True, nullable=False)
    
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

class Franchise(db.Model):
    franchiseId = db.Column(db.String(32), primary_key=True, nullable=False)
    franchiseName = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Enum(YNChoice), nullable=False, default=YNChoice.NA,)
    nationalAssocId = db.Column(db.String(32))

"""
Made alot of assumptions on the nullable fields, so let us see
"""
class Team(db.Model):
    teamId = db.Column(db.String(32), primary_key=True, nullable=False)
    divId = db.Column(db.Enum(Division), nullable=False, default=Division.NONE)
    leagueId = db.Column(db.String(32), nullable=False)
    franchiseId = db.Column(db.ForeignKey('franchise.franchiseId'), nullable=False)
    yearId = db.Column(db.Integer(), nullable=False)

    parkId = db.Column(db.ForeignKey('parks.parkId'), nullable=False)
    attendance = db.Column(db.Integer()) # can be null just cause of lack of info :(

    rank = db.Column(db.Integer(), nullable=False)
    gamesPlayed = db.Column(db.Integer(), nullable=False, default=0)
    homeGamesPlayed = db.Column(db.Integer(), nullable=False, default=0)
    wins = db.Column(db.Integer(), nullable=False, default=0)
    losses = db.Column(db.Integer(), nullable=False, default=0)

    """
    I chose to use the YNChoice enum so we do not have null fields, trying to reduce those to
    a minimum
    """
    divWon = db.Column(db.Enum(YNChoice), nullable=False, default=YNChoice.NA)
    worldCupWon = db.Column(db.Enum(YNChoice), nullable=False, default=YNChoice.NA)
    leagueWon = db.Column(db.Enum(YNChoice), nullable=False, default=YNChoice.NA)
    worldSeriesWon = db.Column(db.Enum(YNChoice), nullable=False, default=YNChoice.NA)

    runs = db.Column(db.Integer(), nullable=False, default=0)
    atBats = db.Column(db.Integer(), nullable=False, default=0)

    batterHit = db.Column(db.Integer(), nullable=False, default=0)
    batterHomeRuns = db.Column(db.Integer(), nullable=False, default=0)
    batterWalks = db.Column(db.Integer(), nullable=False, default=0)

    doubles = db.Column(db.Integer(), nullable=False, default=0)
    triples = db.Column(db.Integer(), nullable=False, default=0)
    strikeouts = db.Column(db.Integer(), nullable=False, default=0)
    stolenBases = db.Column(db.Integer(), nullable=False, default=0)
    caughtStealing = db.Column(db.Integer(), nullable=False, default=0)
    batterHitPitch = db.Column(db.Integer(), nullable=False, default=0)
    sacrificeFlies = db.Column(db.Integer(), nullable=False, default=0)
    opponentRunsScored = db.Column(db.Integer(), nullable=False, default=0)
    earnedRunsAllowed = db.Column(db.Integer(), nullable=False, default=0)
    earnedRunAverage = db.Column(db.Float(), nullable=False, default=0.0) #idk if this should be here tbh
    completeGames = db.Column(db.Integer(), nullable=False, default=0)
    shutouts = db.Column(db.Integer(), nullable=False, default=0)
    saves = db.Column(db.Integer(), nullable=False, default=0)
    ipOuts = db.Column(db.Integer(), nullable=False, default=0)
    hitsAllowed = db.Column(db.Integer(), nullable=False, default=0)
    homerunsAllowed = db.Column(db.Integer(), nullable=False, default=0)
    walksAllowed = db.Column(db.Integer(), nullable=False, default=0)
    pitcherStrikeouts = db.Column(db.Integer(), nullable=False, default=0)
    errors = db.Column(db.Integer(), nullable=False, default=0)
    doublePlays = db.Column(db.Integer(), nullable=False, default=0)
    fieldPercentage = db.Column(db.Float(), nullable=False, default=0.0)

    batterParkFactor = db.Column(db.Integer(), nullable=False, default=0)
    pitcherParkFactor = db.Column(db.Integer(), nullable=False, default=0)





