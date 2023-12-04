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

    sharedawards = SharedAwards(
        personId=line['playerID'],
        awardName=line['awardID'],
        yr=line['yearID'],
        pWon=line['pointsWon'],
        pMax=line['pointsMax'],
        votes=line['votesFirst']
    )
    return sharedawards

def init_awards_share(session):

    try:
        session.query(SharedAwards).delete()
        session.commit()
        print('Cleared Shared Awards!')
    except:
        print('Failed to clear Shared Awards!')
        session.rollback()
        return

    with open('../lahman/AwardsShareManagers.csv', mode='r') as file:
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

    with open('../lahman/AwardsSharePlayers.csv', mode='r') as file:
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