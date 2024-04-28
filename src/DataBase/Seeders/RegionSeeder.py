import pandas as pd

from src.Core.QueryBuilder import QueryBuilder
from src.Models.Region import Region
from src.Models.State import State
from src.Repositories.StateRepository import StateRepository


class RegionSeeder:

    @staticmethod
    def run():
        df_region = pd.DataFrame([
            {'name': 'Norte'},
            {'name': 'Nordeste'},
            {'name': 'Sudeste'},
            {'name': 'Sul'},
            {'name': 'Centro-Oeste'}
        ])

        df_region.to_sql(Region.__tablename__, con=QueryBuilder().engine, if_exists='append', index=False)
