import pandas as pd

from Models.State import State
from src.Core.QueryBuilder import QueryBuilder
from src.Models.Sickness import Sickness


class StateRepository:

    def get_all(self) -> pd.DataFrame:
        # Iniciar uma nova query
        query = QueryBuilder().start_query(State)
        # Converter os resultados para um DataFrame
        return pd.read_sql(query.statement, query.session.bind)
