from sqlalchemy import Column, Integer, String
from comrade_wolf.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(256), unique=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username!r}>'

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id
