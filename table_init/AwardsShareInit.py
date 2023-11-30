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
def create_awards_share(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['teamID'],
        leagueId=line['lgID'],
        yr=line['yearID']).all()
    award_share = AwardsShare(
        awardName=line['awardId'],
        yr=line['yearID'],
        teamId=teams[0].teamId,
        personId=line['playerID'],
        pointsWon=line['pointsWon'],
        pointsMax=line['pointsMax'],
        votesFirst=line['votesFirst'],
    )
    return award_share


def init_awards_share(session):

    try:
        session.query(AwardsShare).delete()
        session.commit()
        print('Cleared Awards Share!')
    except:
        print('Failed to clear Awards Share!')
        session.rollback()
        return

    with open('../lahman/AwardsSharePlayers.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            award_share = create_awards_share(line, session)
            session.add(award_share)
            if i > 1000:
                break
            i+=1
    session.commit()

    with open('../lahman/AwardsShareManagers.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            award_share = create_awards_share(line, session)
            session.add(award_share)
            if i > 1000:
                break
            i+=1
    session.commit()
