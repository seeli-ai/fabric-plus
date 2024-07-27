from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///data.db', echo=False)

with engine.connect() as connection:
    result = connection.execute(text('select "Hallo" '))

    print(result.all())
