from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models import *

import csv

def check_none(v):
    if v == '':
        return None
    return v

def process_line(line):
    new_line = {k: check_none(v) for k, v in line.items()}
    return new_line
def create_fielding(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['teamID'],
        leagueId=line['lgID'],
        yr=line['yearID']).all()
    fielding = Fielding(
        personId=line['playerID'],
        yr=line['yearID'],
        stint=line['stint'],
        teamId=teams[0].teamId,
        position=line['POS'],
        games=line['G'],
        gamesStarted=line['GS'],
        innOuts=line['InnOuts'],
        putouts=line['PO'],
        assists=line['A'],
        errors=line['E'],
        doublePlays=line['DP'],
        passedBalls=line['PB'],
        wildPitches=line['WP'],
        opponentStolenBases=line['SB'],
        opponentsCaughtStealing=line['CS'],
        zoneRating=line['ZR'],

    )
    return fielding

def init_fielding(session):

    try:
        session.query(Fielding).delete()
        session.commit()
        print('Cleared Fielding!')
    except:
        print('Failed to clear Fielding!')
        session.rollback()
        return

    with open('../lahman/Fielding.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            fielding = create_fielding(line, session)
            session.add(fielding)
            # if i > 1000:
            #     break
            # i+=1
    session.commit()
