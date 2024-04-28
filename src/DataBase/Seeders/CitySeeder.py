import pandas as pd
import unicodedata

from src.Repositories.StateRepository import StateRepository
from src.Core.QueryBuilder import QueryBuilder
from src.Models.City import City


class CitySeeder:

    @staticmethod
    def remove_accents_and_uppercase(text):
        # Remove accents and convert to uppercase
        text_without_accents = ''.join(
            char.upper() for char in unicodedata.normalize('NFD', text) if unicodedata.category(char) != 'Mn')
        return text_without_accents

    @staticmethod
    def run():
        df_cities = pd.read_json('cidades.json')
        df_states = StateRepository().get_all()
        df_states['name'] = df_states['name'].apply(CitySeeder.remove_accents_and_uppercase)
        df_cities['state_name'] = df_cities['state_name'].apply(CitySeeder.remove_accents_and_uppercase)

        df_cities = df_cities.merge(
            df_states[['id', 'name']].rename(columns={'name': 'state_name', 'id': 'state_id'}),
            on='state_name',
            how='left'
        ).drop(columns=['state_name'])

        df_cities.to_sql(City.__tablename__, con=QueryBuilder().engine, if_exists='append', index=False)
