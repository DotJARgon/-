from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models import *

import csv

def check_none(v):
    if v == '':
        return None
    return v

def create_date(year, month, day):
    if year is not None and month is not None and day is not None:
        return year + '-' + month + '-' + day
    return None

def process_line(line):
    new_line = {k: check_none(v) for k, v in line.items()}
    return new_line
def create_person(line):
    person = People(
        personId=line['playerID'],
        birthDate=create_date(
            line['birthYear'],
            line['birthMonth'],
            line['birthDay']
        ),
        birthCountry=line['birthCountry'],
        birthState=line['birthState'],
        birthCity=line['birthCity'],

        deathDate=create_date(
            line['deathYear'],
            line['deathMonth'],
            line['deathDay']
        ),
        deathCountry=line['deathCountry'],
        deathState=line['deathState'],
        deathCity=line['deathCity'],

        debutDate=line['debut'],
        finalGameDate=line['finalGame'],
        name=f"{line['nameFirst']} {line['nameLast']}",
        nameGiven=line['nameGiven'],
        weight=line['weight'],
        height=line['height'],
        batHand=Hand.parse(line['bats']),
        throwHand=Hand.parse(line['throws']),


    )
    return person

def init_people(session):

    try:
        session.query(People).delete()
        session.commit()
        print('Cleared Franchises!')
    except:
        print('Failed to clear Franchises!')
        session.rollback()
        return

    with open('../lahman/People.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            person = create_person(line)
            session.add(person)
    session.commit()
