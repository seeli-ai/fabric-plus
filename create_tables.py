from models import Base
from connect_db import engine
import pymysql

print('Creating tables')
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
