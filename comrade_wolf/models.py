from sqlalchemy import Column, Integer, String
from comrade_wolf.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(256), unique=False)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return f'<User {self.name!r}>'

    def get_password(self):
        return self.password
