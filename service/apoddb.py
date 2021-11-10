
from flask import g

from sqlalchemy.orm import sessionmaker

from akit.integration.landscaping.landscape import Landscape

from akit.datum.dbconnection import lookup_database_connection_factory
from akit.datum.dbio import open_apod_database

landscape = Landscape()

def get_apoddb_engine():
    
    apoddb_factory = lookup_database_connection_factory("apod")
    
    if 'dbengine' not in g:
        g.dbengine = open_apod_database(apoddb_factory)

    return g.dbengine

def get_apoddb_session():

    engine = get_apoddb_engine()

    if 'dbsession' not in g:
        Session = sessionmaker(bind=engine)
        g.dbsession = Session()

    return g.dbsession

