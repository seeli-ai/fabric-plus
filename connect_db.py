from sqlalchemy import create_engine
import pymysql
import os


connection_string = os.getenv("DB")
# db = "mysql+pymysql://dbu1394558:NoFog24680!!!@db5016174451.hosting-data.io:3306/dbs13163522"
# connection_string = "mysql+pymysql://avnadmin

# engine = create_engine('sqlite:///data.db', echo=False)
engine = create_engine(
    connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "ca.pem"  # You may need to provide the path to the CA certificate
        }
    }
)

# Base = declarative_base()

# Drop all tables
# Base.metadata.drop_all(engine)

# with engine.connect() as connection:
#    pass
# result = connection.execute(text('select "Hallo" '))
