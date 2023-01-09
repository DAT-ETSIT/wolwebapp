from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from database import Base


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = Column(String(100), unique=True)
    email = Column(String(100))
    password = Column((String(100)))
    admin = Column(Boolean, default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def __repr__(self):
        machine_json = {"id": self.id, "username": self.username, "email": self.email, "password": self.password, "admin": self.admin}
        return str(machine_json)

    def setAdmin(self,admin):
        self.admin = admin

class Machine(Base):
    __tablename__ = 'machines'
    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = Column(String(100), unique=True)
    mac = Column(String(100))
    ip = Column(String(100))
    port = Column(String(100))

    def __init__(self, name, mac, ip, port):
        self.name = name
        self.mac = mac
        self.ip = ip
        self.port = port

    def __repr__(self):
        machine_json = {"id": self.id, "name": self.name, "mac": self.mac, "ip": self.ip, "port": self.port}
        return str(machine_json)


class Ownership(Base):
    __tablename__ = 'ownership'
    id = Column(Integer, primary_key=True)
    machine_id = Column("machine_id", Integer, ForeignKey("machines.id"), nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)

    def __init__(self, machine_id, user_id):
        self.machine_id = machine_id
        self.user_id = user_id

    def __repr__(self):
        owner_json = {"id": self.id, "machine_id": self.machine_id, "user_id": self.user_id}
        return str(owner_json)