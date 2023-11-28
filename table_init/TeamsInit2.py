from time import sleep

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
def create_teams(line, session):
    parks = session.query(Parks).filter(Parks.parkName.ilike(f"%{line['park']}%")).all()
    parkName = line['park']

    if len(parks) == 0:
        parks = session.query(Parks).filter(Parks.parkAlias.ilike(f"%{line['park']}%")).all()
    if len(parks) > 0:
        parkName = parks[0].parkName

    print(line)
    for p in parks:
        print(f"\t{line['park']} : {p.parkName}")
    team = Teams(
        teamNick=line['teamID'],
        teamName=line['name'],
        divId=line['divID'],
        leagueId=line['lgID'],
        franchiseId=line['franchID'],
        yr=line['yearID'],

        parkName=parkName,
        attendance=line['attendance'],

        rank=line['Rank'],
        gamesPlayed=line['G'],
        homeGamesPlayed=line['Ghome'],

        wins=line['W'],
        losses=line['L'],

        divWon=YNChoice.parse(line['divID']),
        worldCupWon=YNChoice.parse(line['WCWin']),
        leagueWon=YNChoice.parse(line['LgWin']),
        worldSeriesWon=YNChoice.parse(line['WSWin']),

        runs=line['R'],
        atBats=line['AB'],

        batterHit=line['H'],
        batterHomeRuns=line['HR'],
        batterWalks=line['BB'],

        doubles=line['2B'],
        triples=line['3B'],

        batterStrikeouts=line['SO'],
        stolenBases=line['SB'],
        caughtStealing=line['CS'],
        batterHitPitch=line['HBP'],
        sacrificeFlies=line['SF'],
        opponentRunsScored=line['RA'],
        earnedRunsAllowed=line['ER'],
        earnedRunAverage=line['ERA'],
        completeGames=line['CG'],
        shutouts=line['SHO'],
        saves=line['SV'],
        ipOuts=line['IPouts'],
        hitsAllowed=line['HA'],
        homerunsAllowed=line['HRA'],
        walksAllowed=line['BBA'],
        pitcherStrikeouts=line['SOA'],
        errors=line['E'],
        doublePlays=line['DP'],
        fieldPercentage=line['FP'],
    
        batterParkFactor=line['BPF'],
        pitcherParkFactor=line['PPF']
    )
    return team

def init_teams(session):

    try:
        session.query(Teams).delete()
        session.commit()
        print('Cleared Teams!')
    except:
        print('Failed to clear Teams!')
        session.rollback()
        return

    with open('../lahman/Teams.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            teams = create_teams(line, session)
            session.add(teams)
    session.commit()
