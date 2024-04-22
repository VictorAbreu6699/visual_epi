from datetime import datetime

import pandas as pd

from src.Models.City import City
from src.Models.Sickness import Sickness
from src.Models.SicknessReport import SicknessReport
from src.Models.State import State
from src.Core.QueryBuilder import QueryBuilder


class SicknessReportRepository:

    @staticmethod
    def get_all(
        sickness_id: list[int] | tuple = None, city_id: list[int] | tuple = None, state_id: list[int] | tuple = None,
        start_date: datetime = None, end_date: datetime = None, columns: list[str] = None
    ) -> pd.DataFrame:
        # Iniciar uma nova query
        query = QueryBuilder().start_query(SicknessReport.date).join(City, City.id == SicknessReport.city_id)
        query = query.join(State, State.id == City.state_id)
        query = query.join(Sickness, Sickness.id == SicknessReport.sickness_id)

        query = query.with_entities(
            Sickness.id.label("sickness_id"), Sickness.name.label("sickness_name"),
            State.id.label('state_id'), State.name.label('state_name'), State.acronym.label('state_acronym'),
            City.id.label('city_id'), City.name.label('city_name'),
            SicknessReport.date, SicknessReport.cases_count
        )

        if sickness_id:
            query = query.filter(SicknessReport.sickness_id.in_(sickness_id))

        if city_id:
            query = query.filter(SicknessReport.city_id.in_(city_id))

        if state_id:
            query = query.filter(State.id.in_(state_id))

        if start_date and end_date:
            query = query.filter(SicknessReport.date.between(start_date, end_date))
        elif start_date:
            query = query.filter(SicknessReport.date >= start_date)
        elif end_date:
            query = query.filter(SicknessReport.date <= end_date)

        # Converter os resultados para um DataFrame
        df = pd.read_sql(query.statement, query.session.bind)

        if columns:
            df = df[columns]

        return df

    @staticmethod
    def insert(dataframe: pd.DataFrame):
        dataframe.to_sql(SicknessReport.__tablename__, con=QueryBuilder().engine, if_exists='append', index=False)
