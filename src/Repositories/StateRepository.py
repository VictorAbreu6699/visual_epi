from datetime import datetime

import pandas as pd

from src.Models.City import City
from src.Models.State import State
from src.Core.QueryBuilder import QueryBuilder


class StateRepository:
    @staticmethod
    def get_all(columns: list[str] = None, region_id: list[int] = None) -> pd.DataFrame:
        # Iniciar uma nova query
        query = QueryBuilder().start_query(State)

        if region_id:
            query = query.filter(State.region_id.in_(region_id))

        # Converter os resultados para um DataFrame
        df = pd.read_sql(query.statement, query.session.bind)

        if columns:
            df = df[columns]

        return df
