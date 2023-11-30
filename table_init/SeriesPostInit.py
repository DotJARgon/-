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
def create_series_post(line, session):
    series = SeriesPost(
        yr=line['yearID'],
        round=line['round'],
        teamIdWinner=['teamIDWinner'],
        teamIdLoser=['teamIDLoser'],
        lgIdWinner=['lgIDWinner'],
        lgIdLoser=['lgIDLoser'],
        wins=line['wins'],
        losses=line['losses'],
        ties=line['ties'],
    )
    return series

def init_series_post(session):

    try:
        session.query(SeriesPost).delete()
        session.commit()
        print('Cleared Series Post!')
    except:
        print('Failed to clear Series Post!')
        session.rollback()
        return

    with open('../lahman/SeriesPost.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            series = create_series_post(line, session)
            session.add(series)
            # if i > 100:
            #     break
            # i+=1
    session.commit()
