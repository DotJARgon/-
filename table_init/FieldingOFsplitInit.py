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


def create_fieldOFsplit(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['teamID'],
        leagueId=line['lgID'],
        yr=line['yearID']).all()
    fieldingOFsplit = FieldingOFSplit(
        personId=line['playerID'],
        yr=line['yearID'],
        stint=line['stint'],
        teamId=teams[0].teamId,
        position=line['POS'],
        games=line['G'],
        gamesStarted=line['GS'],
        innOuts=line['InnOuts'],
        putouts=line['PO'],
        assists=line['A'],
        errors=line['E'],
        doublePlays=line['DP'],

    )
    return fieldingOFsplit


def init_fieldOFsplit(session):
    try:
        session.query(FieldingOFSplit).delete()
        session.commit()
        print('Cleared FieldOFSplit!')
    except:
        print('Failed to clear FieldOFSplit!')
        session.rollback()
        return

    with open('../lahman/FieldingOFsplit.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            fieldOFsplit = create_fieldOFsplit(line, session)
            if fieldOFsplit is not None:
                session.add(fieldOFsplit)
            else:
                print(f"Failed on {line['playerID']}, {line['yearID']}")
            # if fieldOFsplit is not None:
            #     session.add(fieldOFsplit)
            # else:
            #     print(f"Failed on {line['schoolID']}, {line['playerID']}, {line['yearID']}")
            # if i > 1000:
            #     break
            # i+=1
    session.commit()
