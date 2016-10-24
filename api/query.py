import json
from database import db, engine
from models import *
from sqlalchemy.orm import create_session, sessionmaker


Session = sessionmaker(bind=engine)


def add(obj):
    session = Session()
    session.add(obj)
    session.commit()
    users = []
    for instance in session.query(User):
        users.append(instance.first_name)
    return json.dumps(users)

