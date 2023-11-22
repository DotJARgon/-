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
def create_park(line):
    park = Parks(
        parkId=line['park.key'],
        parkName=line['park.name'],
        parkAlias=line['park.alias'],
        parkCountry=line['country'],
        parkState=line['state'],
        parkCity=line['city']
    )
    return park

def init_parks(session):

    try:
        session.query(Parks).delete()
        session.commit()
        print('Cleared Parks!')
    except:
        print('Failed to clear Parks!')
        session.rollback()
        return

    with open('../lahman/Parks.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            park = create_park(line)
            session.add(park)
    session.commit()
