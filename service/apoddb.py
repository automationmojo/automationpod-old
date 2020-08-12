
from flask import g

from sqlalchemy.orm import sessionmaker

from akit.integration.landscaping import Landscape
from akit.datum.dbio import open_apod_postgresql_database

landscape = Landscape()

def get_apoddb_engine():
    
    apoddb_info = landscape.databases["apod"]

    if 'dbengine' not in g:
        g.dbengine = open_apod_postgresql_database(**apoddb_info)

    return g.dbengine

def get_apoddb_session():

    engine = get_apoddb_engine()

    if 'dbsession' not in g:
        Session = sessionmaker(bind=engine)
        g.dbsession = Session()

    return g.dbsession

