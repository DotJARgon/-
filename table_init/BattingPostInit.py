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
def create_batting_post(line, session):
    teams = session.query(Teams).filter_by(teamNick=line['teamID'], yr=line['yearID']).all()
    # if line['playerID'] == 'brainas01':
    #     print(line['playerID'], line['yearID'], line['stint'])
    batting = BattingPost(
        personId=line['playerID'],
        yr=line['yearID'],
        round=line['round'],
        teamId=teams[0].teamId,
        games=line['G'],
        atBats=line['AB'],
        runs=line['R'],
        hits=line['H'],
        doubles=line['2B'],
        triples=line['3B'],
        homeruns=line['HR'],
        runsBattedIn=line['RBI'],
        stolenBases=line['SB'],
        caughtStealing=line['CS'],
        baseOnBalls=line['BB'],
        strikeouts=line['SO'],
        intentionalWalks=line['IBB'],
        hitByPitch=line['HBP'],
        sacrificeHits=line['SH'],
        sacrificeFlies=line['SF'],
        groundedIntoDoublePlays=line['GIDP']
    )
    return batting

def init_batting_post(session):

    try:
        session.query(BattingPost).delete()
        session.commit()
        print('Cleared Batting Post!')
    except:
        print('Failed to clear Batting Post!')
        session.rollback()
        return

    with open('../lahman/BattingPost.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            # print(line)
            pitching = create_batting_post(line, session)
            session.add(pitching)
            # if i > 10000:
            #     break
            # i+=1
    session.commit()
