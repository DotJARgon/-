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
def create_school(line):
    school = Schools(
        schoolId=line['schoolID'],
        name=line['name_full'],
        city=line['city'],
        state=line['state'],
        country=line['country']
    )
    return school

def init_schools(session):

    try:
        session.query(Schools).delete()
        session.commit()
        print('Cleared Schools!')
    except:
        print('Failed to clear Schools!')
        session.rollback()
        return

    with open('../lahman/Schools.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            school = create_school(line)
            session.add(school)
    session.commit()
