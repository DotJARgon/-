from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy import or_
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

def create_awards(line, session):
    leagueId = None
    person = session.query(People).filter(
        People.firstName.ilike(f"%{line['firstName']}%"),
        People.lastName.ilike(f"%{line['lastName']}%")
    ).first()
    if person is not None:
        print("FOUND:", person.personId, person.firstName, person.lastName, "who is", line['firstName'], line['lastName'], line['leagueId'])
        awards = Awards(
            personId=person.personId,
            awardName=line['awardName'],
            yr=line['yr'],
            leagueId=line['leagueId'],
            tie=YNChoice.parse(line['tie']),
            notes=line['notes']
        )
        return awards

    else:
        print("failed on", line['firstName'], line['lastName'])
    return None

def init_awards_2023(session):

    # try:
    #     session.query(Awards).delete()
    #     session.commit()
    #     print('Cleared Awards!')
    # except:
    #     print('Failed to clear Awards!')
    #     session.rollback()
    #     return

    with open('../lahman/AwardsNew.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            # print(line)
            awards = create_awards(line, session)
            if awards is not None:
                session.add(awards)
            # if i > 1000:
            #     break
            # i+=1
            session.commit()
            # if i > 1000:
            #     break
            # i += 1