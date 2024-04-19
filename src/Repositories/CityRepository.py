import pandas as pd

from src.Models.City import City
from src.Core.QueryBuilder import QueryBuilder


class CityRepository:
    @staticmethod
    def get_all() -> pd.DataFrame:
        # Iniciar uma nova query
        query = QueryBuilder().start_query(City)
        # Converter os resultados para um DataFrame
        return pd.read_sql(query.statement, query.session.bind)
