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
def create_allStarFull(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['teamID'],
        leagueId=line['lgID'],
        yr=line['yearID']).all()
    tid = None
    if len(teams) != 0:
        tid = teams[0].teamId
    allStarFull = AllStarFull(
        personId=line['playerID'],
        yr=line['yearID'],
        teamId=tid,
        teamNick=line['teamID'],
        playedGame=line['GP'] == '1',
        gameNum=line['gameNum'],
        gameId=line['gameID'],
        startingPos=line['startingPos']
    )
    return allStarFull

def init_allStarFull(session):

    try:
        session.query(AllStarFull).delete()
        session.commit()
        print('Cleared AllStarFull!')
    except:
        print('Failed to clear AllStarFull!')
        session.rollback()
        return

    with open('../lahman/AllStarFull.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            # print(line)
            allStarFull = create_allStarFull(line, session)
            if allStarFull is not None:
                session.add(allStarFull)
            else:
                print(f"Failed on {line['playerID']}, {line['teamID']}, {line['lgID']}, {line['yearID']}")

            # if i > 1000:
            #     break
            # i+=1
    session.commit()
