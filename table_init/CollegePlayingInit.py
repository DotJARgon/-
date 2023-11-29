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


def create_collegeplay(line, session):
    schools = session.query(Schools).filter_by(
        schoolId=line['schoolID']
    ).all()
    schoolId = None
    if len(schools) != 0:
        schoolId = schools[0].schoolId

    collegeplay = CollegePlaying(
        personId=line['playerID'],
        schoolId=schoolId,
        yr=line['yearID']
    )
    return collegeplay


def init_collegeplay(session):
    try:
        session.query(CollegePlaying).delete()
        session.commit()
        print('Cleared CollegePlaying!')
    except:
        print('Failed to clear CollegePlaying!')
        session.rollback()
        return

    with open('../lahman/CollegePlaying.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            collegeplay = create_collegeplay(line, session)
            session.add(collegeplay)
            # if collegeplay is not None:
            #     session.add(collegeplay)
            # else:
            #     print(f"Failed on {line['schoolID']}, {line['playerID']}, {line['yearID']}")
            # if i > 1000:
            #     break
            # i+=1
    session.commit()
