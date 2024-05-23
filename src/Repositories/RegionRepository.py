from datetime import datetime

import pandas as pd

from src.Models.City import City
from src.Models.Region import Region
from src.Models.State import State
from src.Core.QueryBuilder import QueryBuilder


class RegionRepository:
    @staticmethod
    def get_all(columns: list[str] = []) -> pd.DataFrame:
        # Iniciar uma nova query
        query = QueryBuilder().start_query(Region)
        # Converter os resultados para um DataFrame
        df = pd.read_sql(query.statement, query.session.bind)

        if columns:
            df = df[columns]

        return df
