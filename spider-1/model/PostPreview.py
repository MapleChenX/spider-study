from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

engine = create_engine("mysql+pymysql://root:111111@localhost/spider", echo=True)

metadata = MetaData()
PREVIEW = Table('preview', metadata,
                Column('id', Integer, primary_key=True),
                Column('nickname', String(100)),
                Column('certificate_info', String(100)),
                Column('user_days', String(100)),
                Column('title', String(200)),
                Column('desc', String(500)),
                Column('url', String(100), unique=True),
                Column('actionInfo', String(100)),
                Column('views', Integer)
                )
metadata.create_all(engine)

