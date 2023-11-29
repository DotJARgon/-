from app.models import Managers
from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from ParksInit import init_parks
from TeamsInit2 import init_teams
from FranchiseInit import init_franchises
from SchoolInit import init_schools
from PeopleInit import init_people
from TeamsInit import create_unique_teamid
from PitchingInit import init_pitching
from PitchingPostInit import init_pitching_post
from BattingInit import init_batting
from ManagerInit import init_manager
from FieldingInit import init_fielding
from FieldingPostInit import init_fielding_post
from AppearancesInit import init_appearance
from AllStarInit import init_allStarFull
from HomeGamesInit import init_homegame
from CollegePlayingInit import init_collegeplay
from SalaryInit import init_salary
from HallOfFameInit import init_hallOfFame
from FieldingOFsplitInit import init_fieldOFsplit
from FieldingOFInit import init_fieldingOF
uri = f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['location']}/{mysql['database']}"
engine = sqlalchemy.create_engine(uri)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
# init_parks(session)
# init_franchises(session)
# init_schools(session)
# session.query(Managers).delete()
# init_people(session)
# init_teams(session)
# init_pitching(session)
# init_pitching_post(session)
# init_batting(session)
# create_unique_teamid(session)
# init_manager(session)
# init_appearance(session)
# init_fielding(session)
# init_fielding_post(session)
# init_allStarFull(session)
# init_homegame(session)
# init_collegeplay(session)
# init_salary(session)
# init_hallOfFame(session)
# init_fieldOFsplit(session)
init_fieldingOF(session)
session.close()
