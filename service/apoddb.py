
from flask import g

from sqlalchemy.orm import sessionmaker

from akit.datum.dbio import open_apod_postgresql_database

username = "websvc"
password = "Acess2Data!!"

def get_apoddb_engine():
    if 'dbengine' not in g:
        g.dbengine = open_apod_postgresql_database(username, password)

    return g.dbengine

def get_apoddb_session():

    engine = get_apoddb_engine()

    if 'dbsession' not in g:
        Session = sessionmaker(bind=engine)
        g.dbsession = Session()

    return g.dbsession

