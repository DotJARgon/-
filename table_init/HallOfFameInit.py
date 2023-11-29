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


def create_hallOfFame(line, session):
    people = session.query(People).filter_by(
        personId=line['playerID']
    ).all()
    if len(people) == 0:
        return None
    hallOfFame = HallOfFame(
        personId=line['playerID'],
        yr=line['yearID'],
        votedBy=line['votedBy'],
        totalBallots=line['ballots'],
        totalNeededBallots=line['needed'],
        totalVotes=line['votes'],
        inducted=line['inducted'] == 'Y',
        category=line['category'],
        note=line['needed_note'],
    )
    return hallOfFame


def init_hallOfFame(session):
    try:
        session.query(HallOfFame).delete()
        session.commit()
        print('Cleared HallOfFame!')
    except:
        print('Failed to clear HallOfFame!')
        session.rollback()
        return

    with open('../lahman/HallOfFame.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            hallOfFame = create_hallOfFame(line, session)
            if hallOfFame is not None:
                session.add(hallOfFame)
            else:
                print(f"Failed on {line['playerID']}, {line['yearID']}")
            # if hallOfFame is not None:
            #     session.add(hallOfFame)
            # else:
            #     print(f"Failed on {line['schoolID']}, {line['playerID']}, {line['yearID']}")
            # if i > 1000:
            #     break
            # i+=1
    session.commit()
