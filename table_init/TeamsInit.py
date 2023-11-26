from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models import *

import csv


def collect_teamids(lines):
    teamids = {}
    for l in lines:
        t = l['teamID']
        if not t in teamids:
            teamids[t] = {}
        name = l['name']
        if name not in teamids[t]:
            teamids[t][name] = []
        teamids[t][name].append(int(l['yearID']))

    for k, v in teamids.items():
        print(f"{k}:")
        for k1, v1 in v.items():
            years = sorted(v1)
            print(f"\t{k1} -> {years}")
    return teamids


def check_none(v):
    if v == '':
        return None
    return v


def process_line(line):
    new_line = {k: check_none(v) for k, v in line.items()}
    return new_line


def create_unique_teamid(session):
    lines = []
    with open('../lahman/Teams.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        for l in csvFile:
            lines.append(l)
    t0 = collect_teamids(lines)

    teamids = {}
    for teamNick, teamNames in t0.items():
        for teamName in teamNames:
            abbr = teamName.replace(" ", "")  # remove whitespace
            abbr = ''.join([c for c in abbr if c.isalpha()])  # remove non alphabet
            abbr = abbr[:3].upper()  # trim and capitalize
            i = 1
            while f"{abbr}{i:02d}" in teamids:
                i += 1

            teamids[f"{abbr}{i:02d}"] = {
                "teamName": teamName,
                "teamNick": teamNick,
                "years": t0[teamNick][teamName]
            }

    for teamid, team in teamids.items():
        print(f"{teamid} : {team['teamName']} : {team['teamNick']} : {team['years']}")
        for yr in team['years']:
            t = TeamIds(
                yr=yr,
                teamNick=team['teamNick'],
                teamName=team['teamName'],
                teamId=teamid
            )
            session.add(t)
    session.commit()
    # for teamNick, teamNames in t0:
    #     for

    # with open('../lahman/Teams.csv', mode='r') as file:
    #     csvFile = csv.DictReader(file)
    #     i = 0
    #     for l in csvFile:
    #         line = process_line(l)
    #         print(line)
    #         team = create_team(line, session)
    #         if i > 100:
    #             break
    #         i+=1
    #         session.add(park)
    # session.commit()
