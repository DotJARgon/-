from app import db
import enum

# Unfinished:
#   BattingPost, PitchingPost, Game, School, CollegePlaying, Awards, Hall of Fame, Fielding, Salary, All Star
# Finished
#   User, People, Parks, Franchise, Teams, Appearances, Manager, Batting, Pitching

class Division(enum.Enum):
    W = 1  # west
    E = 2  # east
    C = 3  # central
class YNChoice(enum.Enum):
    Y = 1  # yes
    N = 2  # no
class Hand(enum.Enum):
    L = 1 # left
    R = 2 # right
    B = 3 # ambidextrous

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return self.username


class Parks(db.Model):
    parkId = db.Column(db.String(32), primary_key=True)
    parkName = db.Column(db.String(100))
    parkAlias = db.Column(db.String(100))
    parkCountry = db.Column(db.String(100))
    parkState = db.Column(db.String(100))
    parkCity = db.Column(db.String(100))

class Franchise(db.Model):
    franchiseId = db.Column(db.String(32), primary_key=True)
    franchiseName = db.Column(db.String(100))
    active = db.Column(db.Enum(YNChoice),)
    nationalAssocId = db.Column(db.String(32))
class Teams(db.Model):
    teamId = db.Column(db.String(32), primary_key=True)
    divId = db.Column(db.Enum(Division), default=Division.NONE)
    leagueId = db.Column(db.String(32))
    franchiseId = db.Column(db.ForeignKey('franchise.franchiseId'))
    yr = db.Column(db.Integer())

    parkId = db.Column(db.ForeignKey('parks.parkId'))
    attendance = db.Column(db.Integer())

    rank = db.Column(db.Integer())
    gamesPlayed = db.Column(db.Integer())
    homeGamesPlayed = db.Column(db.Integer())
    wins = db.Column(db.Integer())
    losses = db.Column(db.Integer())

    """
    I chose to use the YNChoice enum so we do not have null fields, trying to reduce those to
    a minimum
    """
    divWon = db.Column(db.Enum(YNChoice))
    worldCupWon = db.Column(db.Enum(YNChoice))
    leagueWon = db.Column(db.Enum(YNChoice))
    worldSeriesWon = db.Column(db.Enum(YNChoice))

    runs = db.Column(db.Integer())
    atBats = db.Column(db.Integer())

    batterHit = db.Column(db.Integer())
    batterHomeRuns = db.Column(db.Integer())
    batterWalks = db.Column(db.Integer())

    doubles = db.Column(db.Integer())
    triples = db.Column(db.Integer())
    batterStrikeouts = db.Column(db.Integer())
    stolenBases = db.Column(db.Integer())
    caughtStealing = db.Column(db.Integer())
    batterHitPitch = db.Column(db.Integer())
    sacrificeFlies = db.Column(db.Integer())
    opponentRunsScored = db.Column(db.Integer())
    earnedRunsAllowed = db.Column(db.Integer())
    earnedRunAverage = db.Column(db.Float()) #idk if this should be here tbh
    completeGames = db.Column(db.Integer())
    shutouts = db.Column(db.Integer())
    saves = db.Column(db.Integer())
    ipOuts = db.Column(db.Integer())
    hitsAllowed = db.Column(db.Integer())
    homerunsAllowed = db.Column(db.Integer())
    walksAllowed = db.Column(db.Integer())
    pitcherStrikeouts = db.Column(db.Integer())
    errors = db.Column(db.Integer())
    doublePlays = db.Column(db.Integer())
    fieldPercentage = db.Column(db.Float())

    batterParkFactor = db.Column(db.Integer())
    pitcherParkFactor = db.Column(db.Integer())

class Appearances(db.Model):
    playerId = db.Column(db.ForeignKey('people.playerId'), primary_key=True)
    yr = db.Column(db.Integer())
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    leagueId = db.Column(db.String(32))
    totalGames = db.Column(db.Integer())
    totalGamesStarted = db.Column(db.Integer())
    gamesBatted = db.Column(db.Integer())
    gamesDefended = db.Column(db.Integer())
    gamesPitcher = db.Column(db.Integer())
    gamesCatcher = db.Column(db.Integer())

    gamesBaseman1 = db.Column(db.Integer())
    gamesBaseman2 = db.Column(db.Integer())
    gamesBaseman3 = db.Column(db.Integer())

    gamesShortStop = db.Column(db.Integer())
    gamesLeftFielder = db.Column(db.Integer())
    gamesCenterFielder = db.Column(db.Integer())
    gamesRightFielder = db.Column(db.Integer())
    gamesOutFielder = db.Column(db.Integer())

    gamesDesignatedHitter = db.Column(db.Integer())
    gamesPinchHitter = db.Column(db.Integer())
    gamesPinchRunner = db.Column(db.Integer())


class People(db.Model):
    playerId = db.Column(db.String(100), primary_key=True)

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

    name = db.Column(db.String(255))
    weight = db.Column(db.Float())
    height = db.Column(db.Float())
    batHand = db.Column(db.Enum(Hand), nullable=True)
    throwHand = db.Column(db.Enum(Hand), nullable=True)
class Player(db.Model):
    playerId = db.Column(db.ForeignKey('people.playerId'), primary_key=True)
    yr = db.Column(db.ForeignKey('people.playerId'), primary_key=True)
class Manager(db.Model):
    playerId = db.Column(db.ForeignKey('people.playerId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    leagueId = db.Column(db.String(32))
    managerialOrder = db.Column(db.Integer()) # inseason = managerial order (perhaps name it that?)
    gamesManaged = db.Column(db.Integer())
    wins = db.Column(db.Integer())
    losses = db.Column(db.Integer())
    rank = db.Column(db.Integer())
    playerManager = db.Column(db.Enum(YNChoice), default=YNChoice.N) #is this necessary?

class Batting(db.Model):
    playerId = db.Column(db.ForeignKey('people.playerId'), primary_key=True)
    yr = db.Column(db.Integer())
    stint = db.Column(db.Integer())
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    leagueId = db.Column(db.String(32))
    games = db.Column(db.Integer())
    atBats = db.Column(db.Integer())
    runs = db.Column(db.Integer())
    hits = db.Column(db.Integer())
    doubles = db.Column(db.Integer())
    triples = db.Column(db.Integer())
    homeruns = db.Column(db.Integer())
    runsBattedIn = db.Column(db.Integer())
    stolenBases = db.Column(db.Integer())
    caughtStealing = db.Column(db.Integer())
    baseOnBalls = db.Column(db.Integer())
    strikeouts = db.Column(db.Integer())
    intentionalWalks = db.Column(db.Integer())
    hitByPitch = db.Column(db.Integer())
    sacrificeHits = db.Column(db.Integer())
    sacrificeFlieds = db.Column(db.Integer())
    groundedIntoDoublePlays = db.Column(db.Integer())
class BattingPost(Batting):
    """"
    identical to batting, fill it later when we decide on final
    paras
    """
    pass

class Pitching(db.Model):
    playerId = db.Column(db.ForeignKey('people.playerId'), primary_key=True)
    yr = db.Column(db.Integer())
    stint = db.Column(db.Integer())
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    leagueId = db.Column(db.String(32))
    wins = db.Column(db.Integer())
    losses = db.Column(db.Integer())
    games = db.Column(db.Integer())
    gamesStarted = db.Column(db.Integer())
    completeGames = db.Column(db.Integer())
    shutouts = db.Column(db.Integer())
    saves = db.Column(db.Integer())
    outsPitched = db.Column(db.Integer())
    hits = db.Column(db.Integer())
    earnedRuns = db.Column(db.Integer())
    homeruns = db.Column(db.Integer())
    walks = db.Column(db.Integer())
    strikeouts = db.Column(db.Integer())
    oppBattingAvg = db.Column(db.Float())
    earnedRunAverage = db.Column(db.Float())
    intentionalWalks = db.Column(db.Integer())
    wildPitches = db.Column(db.Integer())
    battersHitByPitch = db.Column(db.Integer())
    balks = db.Column(db.Integer())
    gamesFinished = db.Column(db.Integer())
    runsAllowed = db.Column(db.Integer())
    opponentSacrifices = db.Column(db.Integer())
    opponentSacrificeFlies = db.Column(db.Integer())
    groundIntoDouble = db.Column(db.Integer())
class PitchingPost(Pitching):
    """
    Same as pitching just need to decide later
    """
    pass

class AllStarFull(db.Model):
    playerId = db.Column(db.ForeignKey('people.playerId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    leagueId = db.Column(db.String(32))
    playedGame = db.Column(db.Boolean())
    gameNum = db.Column(db.Integer())
    gameId = db.Column(db.String(32))
    startingPos = db.Column(db.Integer())

class Fielding(db.Model):
    # playerID,yr,stint,teamID,lgID,POS,G,GS,InnOuts,PO,A,E,DP,PB,WP,SB,CS,ZR
    playerId = db.Column(db.ForeignKey('people.playerId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    leagueId = db.Column(db.String(32))
    stint = db.Column(db.Integer())
    position = db.Column(db.Integer())
    games = db.Column(db.Integer())
    gamesStarted = db.Column(db.Integer())
    innOuts = db.Column(db.Integer())
    putouts = db.Column(db.Integer())
    assists = db.Column(db.Integer())
    errors = db.Column(db.Integer())
    doublePlays = db.Column(db.Integer())
    passedBalls = db.Column(db.Integer())
    wildPitches = db.Column(db.Integer())
    opponentStolenBases = db.Column(db.Integer())
    opponentsCaughtStealing = db.Column(db.Integer())
    zoneRating = db.Column(db.Integer())






