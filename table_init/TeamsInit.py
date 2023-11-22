from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models import *

import csv

uri = f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['location']}/{mysql['database']}"
engine = sqlalchemy.create_engine(uri)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
try:
    session.query(Teams).delete()
    session.commit()
    print('Cleared teams!')
except:
    print('Failed to clear teams!')
    session.rollback()

def create_TeamsObj(line):
    team = Teams(
        teamId=line['teamId'],
        divId=line['divId'],
        leagueId=line['lgId'],
        franchiseId=line['franchId'],
        yr=line['yearId'],
        parkId=line['park']
    )

with open('../lahman/Teams.csv', mode='r') as file:
    csvFile = csv.DictReader(file)
    i = 0
    for lines in csvFile:
        print(lines)
        if i > 100:
            break
        i+=1
