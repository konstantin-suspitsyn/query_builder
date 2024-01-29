from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from comrade_wolf.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(256), unique=False)
    email = Column(String(256), unique=True)
    created_at = Column(DateTime, unique=False, nullable=False)
    updated_at = Column(DateTime, unique=False, nullable=True)

    def __init__(self, username=None, password=None, email=None, created_at=None, updated_at=None):
        self.username = username
        self.password = password
        self.email = email
        if created_at is None:
            self.created_at = datetime.now()
        else:
            self.created_at = created_at
        if updated_at is None:
            self.updated_at = None
        else:
            self.updated_at = updated_at

    def __repr__(self):
        return f'<User {self.username!r}>'

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id
