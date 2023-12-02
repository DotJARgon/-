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
def create_awards_manager(line, session):
    leagueId = None
    manager = session.query(Managers).filter_by(
        personId=line['playerID'],
        yr=line['yearID']
    ).first()
    if manager is not None:
        team = session.query(Teams).filter_by(
            teamId=manager.teamId
        ).first()
        leagueId = team.leagueId
    awards = Awards(
        personId=line['playerID'],
        awardName=line['awardID'],
        yr=line['yearID'],
        leagueId=leagueId,
        tie=line['tie'],
        notes=line['notes']
    )
    return awards

def create_awards_player(line, session):
    leagueId = None
    player = session.query(Appearances).filter_by(
        personId=line['playerID'],
        yr=line['yearID']
    ).first()
    if player is not None:
        team = session.query(Teams).filter_by(
            teamId=player.teamId
        ).first()
        leagueId = team.leagueId
    awards = Awards(
        personId=line['playerID'],
        awardName=line['awardID'],
        yr=line['yearID'],
        leagueId=leagueId,
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
            awards = create_awards_manager(line, session)
            if awards is not None:
                session.add(awards)
            else:
                print(f"Failed on {line['playerID']}, {line['awardID']},{line['lgID']}, {line['yearID']}")
            # if i > 1000:
            #     break
            # i+=1

    with open('../lahman/AwardsPlayers.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            # print(line)
            awards = create_awards_player(line, session)
            if awards is not None:
                session.add(awards)
            else:
                print(f"Failed on {line['playerID']}, {line['awardID']},{line['lgID']}, {line['yearID']}")
    session.commit()
            # if i > 1000:
            #     break
            # i += 1