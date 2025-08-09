from .database import Base
from sqlalchemy import Column, Integer, String

class Hero(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    intelligence = Column(Integer)
    strength = Column(Integer)
    speed = Column(Integer)
    power = Column(Integer)