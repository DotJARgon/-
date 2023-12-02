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
def create_league(line):
    league = Leagues(
        leagueId=line['leagueId'],
        name=line['name'],
        active=YNChoice.parse(line['active'])
    )
    return league

def init_league(session):

    try:
        session.query(Leagues).delete()
        session.commit()
        print('Cleared Leagues!')
    except:
        print('Failed to clear Leagues!')
        session.rollback()
        return

    with open('../lahman/Leagues.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            league = create_league(line)
            if league is not None:
                session.add(league)
            else:
                print(f"Failed on {line['leagueId']}")

            # if i > 1000:
            #     break
            # i+=1
    session.commit()
