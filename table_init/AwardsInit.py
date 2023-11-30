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

# Everything below needs to be changed for awards
def create_awards(line, session):
        #I need to come back here and figure out how we are going to sort this stuff
        # playerID,awardID,yearID,lgID,tie,notes

    awards = Awards(
        personId=line['playerID'],
        award=line['awardId'],
        yr=line['yearID'],
        leagueId=line['lgId'],
        tie=line['tie'],
        notes=line['notes']
    )
    return awards

def init_awards(session):

    try:
        session.query(Awards).delete()
        session.commit()
        print('Cleared Awards!')
    except:
        print('Failed to clear Awards!')
        session.rollback()
        return

    with open('../lahman/AwardsManagers.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            # print(line)
            awards = create_awards(line, session)
            if awards is not None:
                session.add(awards)
            else:
                print(f"Failed on {line['playerID']}, {line['awardID']},{line['lgID']}, {line['yearID']}")

            if i > 1000:
                break
            i+=1

    with open('../lahman/AwardsPlayers.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            # print(line)
            awards = create_awards(line, session)
            if awards is not None:
                session.add(awards)
            else:
                print(f"Failed on {line['playerID']}, {line['awardID']},{line['lgID']}, {line['yearID']}")

            if i > 1000:
                break
            i += 1
    session.commit()