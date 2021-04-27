import sqlalchemy

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('username', sqlalchemy.String(length=100)),
    sqlalchemy.Column('email', sqlalchemy.String(length=50)),
    sqlalchemy.Column('password', sqlalchemy.String(length=32))
)
