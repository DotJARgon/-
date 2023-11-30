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
def create_awards(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['teamID'],
        leagueId=line['lgID'],
        yr=line['yearID']).all()
    award = Awards(
        awardName=line['awardId'],
        personId=line['playerID'],
        yr=line['yearID'],
        teamId=teams[0].teamId,
        tie=line['tie'],
        notes=line['notes']
    )
    return award


def init_awards(session):

    try:
        session.query(Awards).delete()
        session.commit()
        print('Cleared Awards!')
    except:
        print('Failed to clear Awards!')
        session.rollback()
        return

    with open('../lahman/AwardsPlayers.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            award = create_awards(line, session)
            session.add(award)
            if i > 1000:
                break
            i+=1
    session.commit()

    with open('../lahman/AwardsManagers.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            award = create_awards(line, session)
            session.add(award)
            if i > 1000:
                break
            i+=1
    session.commit()
