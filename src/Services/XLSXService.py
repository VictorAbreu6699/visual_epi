from datetime import datetime

import pandas as pd
import unicodedata

from src.Repositories.CityRepository import CityRepository
from src.Repositories.SicknessReportRepository import SicknessReportRepository
from src.Repositories.StateRepository import StateRepository
from src.Repositories.SicknessRepository import SicknessRepository


class XLSXService:
    @staticmethod
    def remove_accents_and_uppercase(text):
        # Remove accents and convert to uppercase
        text_without_accents = ''.join(
            char.upper() for char in unicodedata.normalize('NFD', text) if unicodedata.category(char) != 'Mn')
        return text_without_accents

    @staticmethod
    def generate_default_file() -> str:
        df_all_sickness = SicknessRepository().get_all()
        df_all_cities = CityRepository().get_all()
        df_all_states = StateRepository().get_all()

        df_all_cities = df_all_cities.merge(
            df_all_states.rename(columns={"id": "state_id", "name": "state_name"}),
            how='left',
            on='state_id',
        )

        path = f"src/storage/tmp/modelo_padrao_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
        # Crie um objeto ExcelWriter
        with pd.ExcelWriter(path) as writer:
            # Crie um DataFrame para cada aba
            df_tab1 = pd.DataFrame(columns=[
                'enfermidade', 'municipio', 'data', 'numero_casos'
            ])
            df_tab2 = pd.DataFrame({
                'coluna': [
                    'enfermidade', 'municipio', 'data', 'numero_casos'
                ],
                'formato': [
                    'texto', 'texto, conforme aba "regioes"', 'data', 'número inteiro'
                ],
                'descrição': [
                    'Enfermidade relacionada ao registro', 'Precisa ser conforme a aba "regioes"',
                    'Data do registro, no formato de Data', 'Quantidade de casos constatados na data'
                ]
            })

            df_tab3 = df_all_cities[['name', 'state_name']].rename(columns={'name': 'municipio', 'state_name': 'estado'})

            # Escreve cada DataFrame em uma aba separada
            df_tab1.to_excel(writer, sheet_name='registros', index=False)
            df_tab2.to_excel(writer, sheet_name='dicionario', index=False)
            df_tab3.to_excel(writer, sheet_name='regioes', index=False)

        return path

    @staticmethod
    def import_file_to_database(file_path: str):
        try:
            df_file = pd.read_excel(file_path, sheet_name="registros")
            if df_file.empty:
                return

            df_file.rename(columns={
                "enfermidade": "sickness_name", "municipio": "city_name",
                "data": "date", "numero_casos": "cases_count"
            }, inplace=True)

            df_sickness = SicknessRepository.get_all()
            df_cities = CityRepository.get_all()

            # Para maior compatibilidade durante o merge, remove acentos e converte em letra maiscula os campos de nome.
            df_sickness['name'] = df_sickness['name'].apply(XLSXService.remove_accents_and_uppercase)
            df_cities['name'] = df_cities['name'].apply(XLSXService.remove_accents_and_uppercase)
            df_file['sickness_name'] = df_file['sickness_name'].apply(XLSXService.remove_accents_and_uppercase)
            df_file['city_name'] = df_file['city_name'].apply(XLSXService.remove_accents_and_uppercase)
            df_file['date'] = pd.to_datetime(df_file['date'])

            df_file = df_file.merge(
                df_sickness[['id', 'name']].rename(columns={'name': 'sickness_name', 'id': 'sickness_id'}),
                on='sickness_name',
                how='left'
            )

            df_new_sickness = df_file[df_file['sickness_id'].isnull()]
            if not df_new_sickness.empty:
                try:
                    SicknessRepository.insert(df_new_sickness[['sickness_name']].rename(columns={'sickness_name': 'name'}))
                except Exception as e:
                    raise Exception('Ocorreu um erro ao salvar novas enfermidades.')

                df_sickness = SicknessRepository.get_all()
                df_file = df_file.merge(
                    df_sickness[['id', 'name']].rename(columns={'name': 'sickness_name', 'id': 'sickness_id'}),
                    on='sickness_name',
                    how='left'
                )
                df_file['sickness_id_x'] = df_file['sickness_id_y']
                df_file = df_file.drop(columns=['sickness_id_y']).rename(columns={'sickness_id_x': 'sickness_id'})

            df_file = df_file.drop(columns=['sickness_name'])

            df_file = df_file.merge(
                df_cities[['id', 'name']].rename(columns={'name': 'city_name', 'id': 'city_id'}),
                on='city_name',
                how='left'
            )

            df_cities_dont_found = df_file[df_file['city_id'].isnull()]
            if not df_cities_dont_found.empty:
                cities_dont_found = ', '.join(df_cities_dont_found['city_name'].sort_values().unique().tolist())
                raise Exception(
                    f"Não foi possível identificar as cidades:\n{cities_dont_found}."
                )

            df_sickness_report = SicknessReportRepository.get_all(columns=[
                'sickness_id', 'city_id', 'date', 'cases_count'
            ])

            if not df_sickness_report.empty:
                df_sickness_report['date'] = pd.to_datetime(df_sickness_report['date'])
                df_file = df_file.merge(
                    df_sickness_report,
                    on=['date',  'cases_count',  'sickness_id', 'city_id'],
                    how='left',
                    indicator=True
                )

                df_file = df_file[df_file['_merge'] == 'left_only'].drop(columns=['_merge'])
            df_file = df_file.drop(columns=['city_name'])
            SicknessReportRepository.insert(df_file)

        except ValueError as e:
            raise Exception("O arquivo não está conforme o modelo.")
        except FileNotFoundError:
            raise Exception("O arquivo especificado não foi encontrado.")
        except Exception as e:
            raise Exception(str(e))
