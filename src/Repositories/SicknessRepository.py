import pandas as pd

from src.Core.QueryBuilder import QueryBuilder
from src.Models.Sickness import Sickness


class SicknessRepository:
    @staticmethod
    def get_all() -> pd.DataFrame:
        # Iniciar uma nova query
        query = QueryBuilder().start_query(Sickness)
        # Converter os resultados para um DataFrame
        return pd.read_sql(query.statement, query.session.bind)

    @staticmethod
    def insert(dataframe: pd.DataFrame):
        dataframe.to_sql(Sickness.__tablename__, con=QueryBuilder().engine, if_exists='append', index=False)