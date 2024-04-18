from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)
    capital_id = Column(Integer, nullable=True)
    name = Column(String(255))
    acronym = Column(String(2), nullable=True)

