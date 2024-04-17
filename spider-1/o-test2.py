from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

engine = create_engine("mysql+pymysql://root:111111@localhost/spider", echo=True)
conn = engine.connect()

metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(255)),
              Column('email', String(255))
              )

# C
data = [{'name':'123', 'email': '321'},{'name': '456', 'email': '654'}]
conn.execute(users.insert(), data)
conn.commit()

#R
result = conn.execute(select(users))
for row in result:
    print(row)

#U
conn.execute(users.update().where(users.c.name == '456').values(email='changed'))
conn.commit()

#D
conn.execute(users.delete().where(users.c.name == '123'))
conn.commit()

conn.close()


