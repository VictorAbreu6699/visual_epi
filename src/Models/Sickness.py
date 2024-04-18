from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Sickness(Base):
    __tablename__ = 'sicknesses'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
