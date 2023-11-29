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
def create_homegame(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['team.key'],
        leagueId=line['league.key'],
        yr=line['year.key']).all()
    if len(teams) == 0:
        return None
    homegame = HomeGames(
        yr=line['year.key'],
        teamId=teams[0].teamId,
        firstGame=line['span.first'],
        lastGame=line['span.last'],
        totalGames=line['games'],
        totalOpenings=line['openings'],
        totalAttendance=line['attendance']
    )
    return homegame

def init_homegame(session):

    try:
        session.query(HomeGames).delete()
        session.commit()
        print('Cleared HomeGames!')
    except:
        print('Failed to clear HomeGames!')
        session.rollback()
        return

    with open('../lahman/HomeGames.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            homegame = create_homegame(line, session)
            if homegame is not None:
                session.add(homegame)
            else:
                print(f"Failed on {line['team.key']}, {line['year.key']}")

            # if i > 1000:
            #     break
            # i+=1
    session.commit()
