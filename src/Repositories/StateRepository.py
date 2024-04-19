import pandas as pd

from src.Models.State import State
from src.Core.QueryBuilder import QueryBuilder


class StateRepository:
    @staticmethod
    def get_all() -> pd.DataFrame:
        # Iniciar uma nova query
        query = QueryBuilder().start_query(State)
        # Converter os resultados para um DataFrame
        return pd.read_sql(query.statement, query.session.bind)
