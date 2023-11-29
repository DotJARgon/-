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
def create_fieldingOF(line, session):
    people = session.query(People).filter_by(
        personId=line['playerID']
    ).all()
    if len(people) == 0:
        return None
    fieldingOF = FieldingOF(
        personId=line['playerID'],
        yr=line['yearID'],
        stint=line['stint'],
        gamesLeftField=line['Glf'],
        gamesCenterField=line['Gcf'],
        gamesRightField=line['Grf'],

    )
    return fieldingOF

def init_fieldingOF(session):

    try:
        session.query(FieldingOF).delete()
        session.commit()
        print('Cleared FieldingOF!')
    except:
        print('Failed to clear FieldingOF!')
        session.rollback()
        return

    with open('../lahman/FieldingOF.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            # print(line)
            fieldingOF = create_fieldingOF(line, session)
            if fieldingOF is not None:
                session.add(fieldingOF)
            else:
                print(f"Failed on {line['playerID']}, {line['yearID']}")
            # if i > 1000:
            #     break
            # i+=1
    session.commit()
