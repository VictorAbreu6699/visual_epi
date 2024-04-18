from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import declarative_base

from src.Models.City import City
from src.Models.Sickness import Sickness
from src.Models.State import State

Base = declarative_base()


class SicknessReport(Base):
    __tablename__ = 'sickness_reports'
    id = Column(Integer, primary_key=True)
    sickness_id = Column(Integer, ForeignKey(Sickness.id))
    state_id = Column(Integer, ForeignKey(State.id), nullable=True)
    city_id = Column(Integer, ForeignKey(City.id), nullable=True)
    date = Column(Date)
    cases_count = Column(Integer)
