import numpy as np
import pandas as pd

from src.Core.QueryBuilder import QueryBuilder
from src.Models.State import State
from src.Repositories.StateRepository import StateRepository


class StateSeeder:

    @staticmethod
    def run():
        df_state = pd.DataFrame([
            {'name': 'Acre', 'acronym': 'AC', 'region_id': '1'},
            {'name': 'Alagoas', 'acronym': 'AL', 'region_id': '2'},
            {'name': 'Amapá', 'acronym': 'AP', 'region_id': '1'},
            {'name': 'Amazonas', 'acronym': 'AM', 'region_id': '1'},
            {'name': 'Bahia', 'acronym': 'BA', 'region_id': '2'},
            {'name': 'Ceará', 'acronym': 'CE', 'region_id': '2'},
            {'name': 'Distrito Federal', 'acronym': 'DF', 'region_id': '5'},
            {'name': 'Espírito Santo', 'acronym': 'ES', 'region_id': '3'},
            {'name': 'Goiás', 'acronym': 'GO', 'region_id': '5'},
            {'name': 'Maranhão', 'acronym': 'MA', 'region_id': '2'},
            {'name': 'Mato Grosso', 'acronym': 'MT', 'region_id': '5'},
            {'name': 'Mato Grosso do Sul', 'acronym': 'MS', 'region_id': '5'},
            {'name': 'Minas Gerais', 'acronym': 'MG', 'region_id': '3'},
            {'name': 'Pará', 'acronym': 'PA', 'region_id': '1'},
            {'name': 'Paraíba', 'acronym': 'PB', 'region_id': '2'},
            {'name': 'Paraná', 'acronym': 'PR', 'region_id': '4'},
            {'name': 'Pernambuco', 'acronym': 'PE', 'region_id': '2'},
            {'name': 'Piauí', 'acronym': 'PI', 'region_id': '2'},
            {'name': 'Rio de Janeiro', 'acronym': 'RJ', 'region_id': '3'},
            {'name': 'Rio Grande do Norte', 'acronym': 'RN', 'region_id': '2'},
            {'name': 'Rio Grande do Sul', 'acronym': 'RS', 'region_id': '4'},
            {'name': 'Rondônia', 'acronym': 'RO', 'region_id': '1'},
            {'name': 'Roraima', 'acronym': 'RR', 'region_id': '1'},
            {'name': 'Santa Catarina', 'acronym': 'SC', 'region_id': '4'},
            {'name': 'São Paulo', 'acronym': 'SP', 'region_id': '3'},
            {'name': 'Sergipe', 'acronym': 'SE', 'region_id': '2'},
            {'name': 'Tocantins', 'acronym': 'TO', 'region_id': '1'}
        ])

        df_state.to_sql(State.__tablename__, con=QueryBuilder().engine, if_exists='append', index=False)
