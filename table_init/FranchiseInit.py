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
def create_franchise(line):
    franch = Franchises(
        franchiseId=line['franchID'],
        franchiseName=line['franchName'],
        active=YNChoice.parse(line['active']),
        nationalAssocId=line['NAassoc']
    )
    return franch

def init_franchises(session):

    try:
        session.query(Parks).delete()
        session.commit()
        print('Cleared Franchises!')
    except:
        print('Failed to clear Franchises!')
        session.rollback()
        return

    with open('../lahman/TeamsFranchises.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            franch = create_franchise(line)
            session.add(franch)
    session.commit()
