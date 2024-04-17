from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, declarative_base

engine = create_engine("mysql+pymysql://root:111111@localhost/spider")
session = Session(bind=engine)

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __str__(self):
        return f'User(id={self.id}, name={self.name}, email={self.email})'

# C
new_user = User(name='Alice', email='alice@example.com')
session.add(new_user)
session.commit()

# R
user = session.query(User).filter(User.name == 'Alice').first()
print(user)

# U
user = session.query(User).filter(User.name == 'Alice').first()
user.email = 'new_email@example.com'
session.commit()

# D
user = session.query(User).filter(User.name == 'Alice').first()
session.delete(user)
session.commit()

session.close()

