import pandas as pd

from src.Core.QueryBuilder import QueryBuilder
from src.Models.Sickness import Sickness


class SicknessSeeder:
    @staticmethod
    def run():
        df_sicknesses = pd.DataFrame([
            {
                "name": "Dengue"
            },
            {
                "name": "Covid-19"
            }
        ])

        df_sicknesses.to_sql(Sickness.__tablename__, con=QueryBuilder().engine, if_exists='append', index=False)
