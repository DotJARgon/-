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
    # new_line = {k: check_league(v) for k, v in new_line.items()}
    return new_line
def create_series_post(line, session):
    teamWinner = session.query(Teams).filter_by(
        teamNick=line['teamIDwinner'],
        leagueId=line['lgIDwinner'],
        yr=line['yearID']
    ).first()
    teamLoser = session.query(Teams).filter_by(
        teamNick=line['teamIDloser'],
        leagueId=line['lgIDloser'],
        yr=line['yearID']
    ).first()

    series = SeriesPost(
        yr=line['yearID'],
        round=line['round'],
        teamIdWinner=teamWinner.teamId,
        teamIdLoser=teamLoser.teamId,
        leagueIdWinner=teamWinner.leagueId,
        leagueIdLoser=teamLoser.leagueId,
        wins=line['wins'],
        losses=line['losses'],
        ties=line['ties'],
    )
    print(series.__dict__)
    return series

def init_series_post(session):

    # try:
    #     session.query(SeriesPost).delete()
    #     session.commit()
    #     print('Cleared Series Post!')
    # except:
    #     print('Failed to clear Series Post!')
    #     session.rollback()
    #     return

    with open('../lahman/SeriesPost.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            series = create_series_post(line, session)
            session.add(series)
            # if i > 100:
            #     break
            # i+=1
            session.commit()
