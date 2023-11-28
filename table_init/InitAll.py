from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from ParksInit import init_parks
from TeamsInit2 import init_teams
from FranchiseInit import init_franchises
from SchoolInit import init_schools
from PeopleInit import init_people
from TeamsInit import create_unique_teamid

uri = f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['location']}/{mysql['database']}"
engine = sqlalchemy.create_engine(uri)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
# init_parks(session)
# init_franchises(session)
# init_schools(session)
# init_people(session)
# init_teams(session)
# create_unique_teamid(session)
session.close()