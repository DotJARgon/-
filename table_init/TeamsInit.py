from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models import *

import csv

def generate_unique_teamid(lines):
    teamids = {}
    for l in lines:
        t = l['teamID']
        if not t in teamids:
            teamids[t] = {}
        name = l['name']
        if name not in teamids[t]:
            teamids[t][name] = []
        teamids[t][name].append(l)

    for k, v in teamids.items():
        print(f"{k}:")
        for k1, v1 in v.items():
            print(f"\t{k1} -> {len(v1)}")

def check_none(v):
    if v == '':
        return None
    return v

def process_line(line):
    new_line = {k: check_none(v) for k, v in line.items()}
    return new_line
def create_team(line):
    team = Teams(
        teamId=line['teamId'],
        parkName=line['park.name'],
        parkAlias=line['park.alias'],
        parkCountry=line['country'],
        parkState=line['state'],
        parkCity=line['city']
    )
    return team

def init_teams(session):

    try:
        session.query(Teams).delete()
        session.commit()
        print('Cleared Teams!')
    except:
        print('Failed to clear Teams!')
        session.rollback()
        return
    with open('../lahman/Teams.csv', mode='r') as file:
        lines = []
        csvFile = csv.DictReader(file)
        for l in csvFile:
            lines.append(l)
    generate_unique_teamid(lines)

    # with open('../lahman/Teams.csv', mode='r') as file:
    #     csvFile = csv.DictReader(file)
    #     i = 0
    #     for l in csvFile:
    #         line = process_line(l)
    #         print(line)
    #         team = create_team(line, session)
    #         if i > 100:
    #             break
    #         i+=1
    #         session.add(park)
    # session.commit()
