import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ.get('DATABASE_URL') 
engine = create_engine(DATABASE_URL)
DBSessionBuilder = sessionmaker(bind = engine)

Base = declarative_base()

class User(Base):
	__tablename__ = 'userdata'
	
	userid = Column('userid', String(20), primary_key = True)

	photolink = Column('photolink', String(255), default = None)
	n_clusters = Column('n_clusters', Integer, default = None)