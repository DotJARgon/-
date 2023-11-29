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

def create_manager_half(line, session):
    teams = session.query(Teams).filter_by(teamNick=line['teamID'], leagueId=line["lgID"], yr=line['yearID']).all()
    managers = session.query(Managers).filter_by(
        personId=line["playerID"],
        yr=line["yearID"],
        half=0,
        teamId=teams[0].teamId
    ).all()

    manager = Managers(
        personId=line["playerID"],
        yr=line["yearID"],
        teamId=teams[0].teamId,
        half=line["half"],
        managerialOrder=line["inseason"],
        gamesManaged=line["G"],
        wins=line["W"],
        losses=line["L"],
        rank=line["rank"],
        playerManager=managers[0].playerManager,
    )
    return manager
def create_manager(line, session):
    teams = session.query(Teams).filter_by(
        teamNick=line['teamID'],
        leagueId=line['lgID'],
        yr=line['yearID']).all()
    manager = Managers(
        personId=line["playerID"],
        yr=line["yearID"],
        teamId=teams[0].teamId,
        managerialOrder=line["inseason"],
        gamesManaged=line["G"],
        wins=line["W"],
        losses=line["L"],
        rank=line["rank"],
        playerManager=YNChoice.parse(line["plyrMgr"]),
        half=0
    )
    return manager

def init_manager(session):

    try:
        session.query(Managers).delete()
        session.commit()
        print('Cleared Managers!')
    except:
        print('Failed to clear Managers!')
        session.rollback()
        return

    with open('../lahman/Managers.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            manager = create_manager(line, session)
            session.add(manager)
            # if i > 500:
            #     break
            # i+=1
    session.commit()
    half = []
    with open('../lahman/ManagersHalf.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        i = 0
        for l in csvFile:
            line = process_line(l)
            print(line)
            manager = create_manager_half(line, session)
            half.append(manager)
            session.add(manager)
            # if i > 10000:
            #     break
            # i+=1
    session.commit()

    for m in half:
        m_del = session.query(Managers).filter_by(
            personId=m.personId,
            yr=m.yr,
            half=0,
            teamId=m.teamId
        )
        m_del.delete(synchronize_session=False)
