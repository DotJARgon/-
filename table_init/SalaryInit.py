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


def create_salary(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['teamID'],
        leagueId=line['lgID'],
        yr=line['yearID']).all()
    teamId = None
    if len(teams) != 0:
        teamId = teams[0].teamId
    salary = Salaries(
        personId=line['playerID'],
        teamId=teamId,
        yr=line['yearID'],
        salary=line['salary']
    )
    return salary


def init_salary(session):
    try:
        session.query(Salaries).delete()
        session.commit()
        print('Cleared Salaries!')
    except:
        print('Failed to clear Salaries!')
        session.rollback()
        return

    with open('../lahman/Salaries.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            salary = create_salary(line, session)
            session.add(salary)
            # if salary is not None:
            #     session.add(salary)
            # else:
            #     print(f"Failed on {line['schoolID']}, {line['playerID']}, {line['yearID']}")
            # if i > 1000:
            #     break
            # i+=1
    session.commit()
