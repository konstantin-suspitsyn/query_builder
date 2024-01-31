from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from comrade_wolf.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(256), unique=False)
    email = Column(String(256), unique=True)
    created_at = Column(DateTime, unique=False, nullable=False)
    updated_at = Column(DateTime, unique=False, nullable=True)
    is_active = Column(Boolean, unique=False, nullable=False)

    def __init__(self, username=None, password=None, email=None, created_at=None, updated_at=None, is_active=None):
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
        if is_active is None:
            self.is_active = False
        else:
            self.is_active = is_active

    def __repr__(self):
        return f'<User {self.username!r}>'

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id


class ActivationCode(Base):
    __tablename__ = "activation_code"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    activation_code = Column(String(256), unique=True)
    is_active = Column(Boolean, unique=False, nullable=False)
    created_at = Column(DateTime, unique=False, nullable=False)
    updated_at = Column(DateTime, unique=False, nullable=True)

    def __init__(self, user_id=None, activation_code=None, is_active=None, updated_at=None):
        self.user_id = user_id
        self.activation_code = activation_code
        if is_active is None:
            self.is_active = False
        else:
            self.is_active = is_active

        self.created_at = datetime.now()
        if updated_at is not None:
            self.updated_at = updated_at
