from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import enum


class Division(enum.Enum):
    W = 1  # west
    E = 2  # east
    C = 3  # central
class YNChoice(enum.Enum):
    Y = 1  # yes
    N = 2  # no
    X = 3  # not applicable
    @staticmethod
    def parse(c):
        if c == 'Y':
            return YNChoice.Y
        elif c == 'N':
            return YNChoice.N
        elif c == 'NA':
            return YNChoice.X
        return None
class Hand(enum.Enum):
    L = 1  # left
    R = 2  # right
    B = 3  # ambidextrous
    @staticmethod
    def parse(h):
        if h == 'L':
            return Hand.L
        elif h == 'R':
            return Hand.R
        elif h == 'B':
            return Hand.B
        return None


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    count = db.Column(db.Integer(), default=0, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Parks(db.Model):
    parkId = db.Column(db.String(32), primary_key=True)
    parkName = db.Column(db.String(255), index=True)
    parkAlias = db.Column(db.String(255))
    parkCountry = db.Column(db.String(255))
    parkState = db.Column(db.String(255))
    parkCity = db.Column(db.String(255))


class Franchises(db.Model):
    franchiseId = db.Column(db.String(32), primary_key=True)
    franchiseName = db.Column(db.String(100))
    active = db.Column(db.Enum(YNChoice))
    nationalAssocId = db.Column(db.String(32))

class Leagues(db.Model):
    leagueId = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(50))
    active = db.Column(db.Enum(YNChoice))

class Teams(db.Model):
    teamId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    yr = db.Column(db.Integer())
    teamNick = db.Column(db.String(32))
    teamName = db.Column(db.String(50))
    divId = db.Column(db.Enum(Division))
    leagueId = db.Column(db.ForeignKey('leagues.leagueId'))
    # leagueId = db.Column(db.String(32))
    franchiseId = db.Column(db.ForeignKey('franchises.franchiseId'))
    unique = db.UniqueConstraint(yr, teamNick, leagueId)

    # parkName = db.Column(db.ForeignKey('parks.parkName'))
    parkName = db.Column(db.String(255))
    attendance = db.Column(db.Integer())

    rank = db.Column(db.Integer())
    gamesPlayed = db.Column(db.Integer())
    homeGamesPlayed = db.Column(db.Integer())
    wins = db.Column(db.Integer())
    losses = db.Column(db.Integer())

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
    earnedRunAverage = db.Column(db.Float())  # idk if this should be here tbh
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
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
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
    personId = db.Column(db.String(100), primary_key=True)
    birthDate = db.Column(db.Date())
    # birthYear = db.Column(db.Integer())
    # birthMonth = db.Column(db.Integer())
    # birthDay = db.Column(db.Integer())
    birthCountry = db.Column(db.String(100))
    birthState = db.Column(db.String(100))
    birthCity = db.Column(db.String(100))

    deathDate = db.Column(db.Date())
    # deathYear = db.Column(db.Integer())
    # deathMonth = db.Column(db.Integer())
    # deathDay = db.Column(db.Integer())
    deathCountry = db.Column(db.String(100))
    deathState = db.Column(db.String(100))
    deathCity = db.Column(db.String(100))

    debutDate = db.Column(db.Date())
    # debutYear = db.Column(db.Integer())
    # debutMonth = db.Column(db.Integer())
    # debutDay = db.Column(db.Integer())
    # debutCountry = db.Column(db.String(100))
    # debutState = db.Column(db.String(100))
    # debutCity = db.Column(db.String(100))

    finalGameDate = db.Column(db.Date())
    # finalGameYear = db.Column(db.Integer())
    # finalGameMonth = db.Column(db.Integer())
    # finalGameDay = db.Column(db.Integer())
    # finalGameCountry = db.Column(db.String(100))
    # finalGameState = db.Column(db.String(100))
    # finalGameCity = db.Column(db.String(100))

    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    nameGiven = db.Column(db.String(255))
    weight = db.Column(db.Float())
    height = db.Column(db.Float())
    batHand = db.Column(db.Enum(Hand), nullable=True)
    throwHand = db.Column(db.Enum(Hand), nullable=True)
class Managers(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    half = db.Column(db.Integer, primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'), primary_key=True)
    managerialOrder = db.Column(db.Integer(), primary_key=True)  # inseason = managerial order (perhaps name it that?)
    gamesManaged = db.Column(db.Integer())
    wins = db.Column(db.Integer())
    losses = db.Column(db.Integer())
    rank = db.Column(db.Integer())
    playerManager = db.Column(db.Enum(YNChoice), default=YNChoice.N)  # is this necessary?


class Batting(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    stint = db.Column(db.Integer(), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
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
    sacrificeFlies = db.Column(db.Integer())
    groundedIntoDoublePlays = db.Column(db.Integer())
class BattingPost(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    round = db.Column(db.String(32), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
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
    sacrificeFlies = db.Column(db.Integer())
    groundedIntoDoublePlays = db.Column(db.Integer())

class Pitching(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    stint = db.Column(db.Integer(), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
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
    battersFacedByPitch = db.Column(db.Integer())
    gamesFinished = db.Column(db.Integer())
    runsAllowed = db.Column(db.Integer())
    opponentSacrifices = db.Column(db.Integer())
    opponentSacrificeFlies = db.Column(db.Integer())
    groundIntoDouble = db.Column(db.Integer())
class PitchingPost(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    # stint = db.Column(db.Integer(), primary_key=True)
    round = db.Column(db.String(32), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
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
    battersFacedByPitch = db.Column(db.Integer())
    gamesFinished = db.Column(db.Integer())
    runsAllowed = db.Column(db.Integer())
    opponentSacrifices = db.Column(db.Integer())
    opponentSacrificeFlies = db.Column(db.Integer())
    groundIntoDouble = db.Column(db.Integer())
class Fielding(db.Model):
    # personId,yr,stint,teamNick,lgID,POS,G,GS,InnOuts,PO,A,E,DP,PB,WP,SB,CS,ZR
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    stint = db.Column(db.Integer(), primary_key=True)
    position = db.Column(db.String(10), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
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
class FieldingPost(db.Model):
    # personId,yr,stint,teamNick,lgID,POS,G,GS,InnOuts,PO,A,E,DP,PB,WP,SB,CS,ZR
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    round = db.Column(db.String(10), primary_key=True)
    position = db.Column(db.String(10), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    games = db.Column(db.Integer())
    gamesStarted = db.Column(db.Integer())
    innOuts = db.Column(db.Integer())
    putouts = db.Column(db.Integer())
    assists = db.Column(db.Integer())
    errors = db.Column(db.Integer())
    doublePlays = db.Column(db.Integer())
    passedBalls = db.Column(db.Integer())
    opponentStolenBases = db.Column(db.Integer())
    opponentsCaughtStealing = db.Column(db.Integer())
class FieldingOF(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    stint = db.Column(db.Integer(), primary_key=True)
    gamesLeftField = db.Column(db.Integer())
    gamesCenterField = db.Column(db.Integer())
    gamesRightField = db.Column(db.Integer())

class FieldingOFSplit(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    stint = db.Column(db.Integer(), primary_key=True)
    position = db.Column(db.String(10), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    games = db.Column(db.Integer())
    gamesStarted = db.Column(db.Integer())
    innOuts = db.Column(db.Integer())
    putouts = db.Column(db.Integer())
    assists = db.Column(db.Integer())
    errors = db.Column(db.Integer())
    doublePlays = db.Column(db.Integer())

class AllStarFull(db.Model):
    allstarfullId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    personId = db.Column(db.ForeignKey('people.personId'))
    yr = db.Column(db.Integer())
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    teamNick = db.Column(db.String(32))
    playedGame = db.Column(db.Boolean())
    gameNum = db.Column(db.Integer())
    gameId = db.Column(db.String(32))
    startingPos = db.Column(db.Integer())


class HomeGames(db.Model):
    homegameId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    yr = db.Column(db.Integer())
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    firstGame = db.Column(db.Date())
    lastGame = db.Column(db.Date())
    totalGames = db.Column(db.Integer())
    totalOpenings = db.Column(db.Integer())
    totalAttendance = db.Column(db.Integer())


class Schools(db.Model):
    schoolId = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(255))
    city = db.Column(db.String(55))
    state = db.Column(db.String(55))
    country = db.Column(db.String(55))
class CollegePlaying(db.Model):
    collegePlayingId = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    schoolId = db.Column(db.ForeignKey('schools.schoolId'))
    personId = db.Column(db.ForeignKey('people.personId'))
    yr = db.Column(db.Integer())
    unique = db.UniqueConstraint(schoolId, personId, yr)


class Salaries(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    teamId = db.Column(db.ForeignKey('teams.teamId'), primary_key=True)
    salary = db.Column(db.Float())


class Awards(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    awardName = db.Column(db.String(255))
    personId = db.Column(db.ForeignKey('people.personId'))
    yr = db.Column(db.Integer())
    teamId = db.Column(db.ForeignKey('teams.teamId'))
    tie = db.Column(db.Boolean())
    notes = db.Column(db.String(255))
    unique = db.UniqueConstraint(yr, personId, awardName)


class HallOfFame(db.Model):
    personId = db.Column(db.ForeignKey('people.personId'), primary_key=True)
    yr = db.Column(db.Integer(), primary_key=True)
    votedBy = db.Column(db.String(255), primary_key=True)
    totalBallots = db.Column(db.Integer())
    totalNeededBallots = db.Column(db.Integer())
    totalVotes = db.Column(db.Integer())
    inducted = db.Column(db.Boolean())
    category = db.Column(db.String(32))
    note = db.Column(db.String(100))
