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
def create_appearance(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['teamID'],
        leagueId=line['lgID'],
        yr=line['yearID']).all()
    # print('\t',teams[0].teamId)
    appearance = Appearances(
        personId=line['playerID'],
        teamId=teams[0].teamId,
        yr=line['yearID'],
        totalGames=line['G_all'],
        totalGamesStarted=line['GS'],
        gamesBatted=line['G_batting'],
        gamesDefended=line['G_defense'],
        gamesPitcher=line['G_p'],
        gamesCatcher=line['G_c'],
        gamesBaseman1=line['G_1b'],
        gamesBaseman2=line['G_2b'],
        gamesBaseman3=line['G_3b'],
        gamesShortStop=line['G_ss'],
        gamesLeftFielder=line['G_lf'],
        gamesCenterFielder=line['G_cf'],
        gamesRightFielder=line['G_rf'],
        gamesOutFielder=line['G_of'],
        gamesDesignatedHitter=line['G_dh'],
        gamesPinchHitter=line['G_ph'],
        gamesPinchRunner=line['G_pr']
    )
    return appearance

def init_appearance(session):

    try:
        session.query(Appearances).delete()
        session.commit()
        print('Cleared Appearances!')
    except:
        print('Failed to clear Appearances!')
        session.rollback()
        return

    with open('../lahman/Appearances.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            appearance = create_appearance(line, session)
            session.add(appearance)
            if i > 1000:
                break
            i+=1
            session.commit()
