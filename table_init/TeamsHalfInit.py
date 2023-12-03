from app.models import *

import csv


def check_none(v):
    if v == '':
        return None
    return v


def process_line(line):
    new_line = {k: check_none(v) for k, v in line.items()}
    return new_line


def create_teams_half(line, session):
    team = session.query(Teams).filter_by(teamNick=line['teamID'], leagueId=line["lgID"], yr=line['yearID']).first()

    team_half = TeamsHalf(
        teamId=team.teamId,
        yr=line['yearID'],
        leagueId=line['lgID'],
        half=line['Half'],
        divId=line['divID'],
        divWon=line['DivWin'],
        rank=line['Rank'],
        gamesPlayed=line['G'],
        wins=line['W'],
        losses=line['L'],
    )
    return team_half


def init_teams_half(session):
    try:
        session.query(TeamsHalf).delete()
        session.commit()
        print('Cleared TeamsHalf!')
    except:
        print('Failed to clear TeamsHalf!')
        session.rollback()
        return

    with open('../lahman/TeamsHalf.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            teams = create_teams_half(line, session)
            session.add(teams)
            session.commit()
