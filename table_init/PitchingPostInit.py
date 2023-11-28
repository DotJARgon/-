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
def create_pitching_post(line, session):
    teams = session.query(Teams).filter_by(teamNick=line['teamID'], yr=line['yearID']).all()
    # if line['playerID'] == 'brainas01':
    # print(line['playerID'], line['yearID'], line['round'])
    pitching = PitchingPost(
        personId=line['playerID'],
        yr=line['yearID'],
        round=line['round'],
        teamId=teams[0].teamId,
        wins=line['W'],
        losses=line['L'],
        games=line['G'],
        gamesStarted=line['GS'],
        completeGames=line['CG'],
        shutouts=line['SHO'],
        saves=line['SV'],
        outsPitched=line['IPouts'],
        hits=line['H'],
        earnedRuns=line['ER'],
        homeruns=line['HR'],
        walks=line['BB'],
        strikeouts=line['SO'],
        oppBattingAvg=line['BAOpp'],
        earnedRunAverage=line['ERA'],
        intentionalWalks=line['IBB'],
        wildPitches=line['WP'],
        battersHitByPitch=line['HBP'],
        balks=line['BK'],
        battersFacedByPitch=line['BFP'],
        gamesFinished=line['GF'],
        runsAllowed=line['R'],
        opponentSacrifices=line['SH'],
        opponentSacrificeFlies=line['SF'],
        groundIntoDouble=line['GIDP']
    )
    return pitching

def init_pitching_post(session):

    try:
        session.query(PitchingPost).delete()
        session.commit()
        print('Cleared Pitching Post!')
    except:
        print('Failed to clear Pitching Post!')
        session.rollback()
        return

    with open('../lahman/PitchingPost.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            # print(line)
            pitching = create_pitching_post(line, session)
            session.add(pitching)
            # if i > 100:
            #     break
            # i+=1
    session.commit()
