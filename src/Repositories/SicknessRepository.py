import pandas as pd

from src.Core.QueryBuilder import QueryBuilder
from src.Models.Sickness import Sickness


class SicknessRepository:

    def get_all(self) -> pd.DataFrame:
        # Iniciar uma nova query
        query = QueryBuilder().start_query(Sickness)
        # Converter os resultados para um DataFrame
        return pd.read_sql(query.statement, query.session.bind)
