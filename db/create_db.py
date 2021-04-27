from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

DB_URL = 'postgresql://admin:admin@localhost/users'
engine = create_engine(DB_URL)

metadata = MetaData(engine)

table = Table('users', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('username', String(32), unique=True, index=True),
              Column('email', String(50)),
              Column('password', String(80)))

table.drop(engine)
table.create(engine)

for _t in metadata.tables:
    print("Table: ", _t)
