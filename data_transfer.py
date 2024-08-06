import sqlite3
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# SQLite connection
sqlite_conn = sqlite3.connect('data.db')
sqlite_cursor = sqlite_conn.cursor()

# MySQL connection
connection_string = ""

# engine = create_engine('sqlite:///data.db', echo=False)
mysql_engine = create_engine(
    connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "ca.pem"  # You may need to provide the path to the CA certificate
        }
    }
)

mysql_conn = mysql_engine.connect()

# Create a session
Session = sessionmaker(bind=mysql_engine)
session = Session()

# Get the MetaData
metadata = MetaData()
metadata.reflect(bind=mysql_engine)

# Function to transfer data for a single table
def transfer_table(table_name):
    # Fetch all data from SQLite
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()

    # Get column names
    sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in sqlite_cursor.fetchall()]

    # Get the SQLAlchemy Table object
    table = Table(table_name, metadata, autoload_with=mysql_engine)

    # Insert data into MySQL
    for row in rows:
        data = dict(zip(columns, row))
        insert_stmt = table.insert().values(**data)
        mysql_conn.execute(insert_stmt)

    mysql_conn.commit()
    print(f"Transferred {len(rows)} rows to {table_name}")

# List of tables to transfer
tables = ['users', 'prompts', 'providers', "models", "inputs"]  # Add all your table names here

# Transfer each table
for table in tables:
    transfer_table(table)

# Close connections
sqlite_conn.close()
mysql_conn.close()
session.close()

print("Data transfer completed.")