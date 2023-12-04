from app.models import User
from csi3335F2023 import mysql
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

uri = f"mysql+pymysql://{mysql['user']}:{mysql['password']}@{mysql['location']}/{mysql['database']}"
engine = sqlalchemy.create_engine(uri)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

username = input("Enter your new admin username: ")

password = input("Enter admin password: ")
retyped = input("Enter admin password again: ")

if password != retyped:
    print('Password and Retyped password do not match, please try again')

confirm = input(f"Confirm to create admin {username}, this will delete previous admin account, enter in 'Y' for yes, anything else for no: ")
if confirm != 'Y':
    exit(0)

print('Deleting previous admin')
session.query(User).filter_by(
    is_admin=True
).delete()
session.commit()
print('Creating new admin')
user = User(username=username)
user.set_password(password)
user.is_admin = True
session.add(user)
session.commit()

