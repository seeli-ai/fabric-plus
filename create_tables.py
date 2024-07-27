from models import Base
from connect_db import engine

print('Creating tables')
Base.metadata.create_all(bind=engine)
