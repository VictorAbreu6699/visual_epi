from datetime import datetime

import pandas as pd

from src.Repositories.SicknessRepository import SicknessRepository


class XLSXService:
    @staticmethod
    def generate_default_file() -> str:
        df_all_sickness = SicknessRepository().get_all()

        path = f"src/storage/tmp/modelo_padrao_{datetime.now().strftime('d_m_Y')}.xlsx"
        # Crie um objeto ExcelWriter
        with pd.ExcelWriter(path) as writer:
            # Crie um DataFrame para cada aba
            df_tab1 = pd.DataFrame(columns=[
                'enfermidade', 'estado', 'municipio', 'data', 'numero_casos'
            ])
            df_tab2 = pd.DataFrame({
                'coluna': [
                    'enfermidade', 'estado', 'municipio', 'data', 'numero_casos'
                ],
                'formato': [
                    'texto', 'texto',
                    'texto, conforme aba "regiões"', '2024-01-01 (Y-m-d)', 'inteiro'
                ],
                'descrição': [
                    'Precisa ser conforme a aba "enfermidades"', 'Precisa ser conforme a aba "regiões"',
                    'Precisa ser conforme a aba "regiões"', 'data do registro, no formato Y-m-d, Ano-Mês-Dia',
                    'quantidade de casos constatados na data'
                ]
            })

            df_tab3 = df_all_sickness[['name']].rename(columns={'name': 'nome'})

            # Escreva cada DataFrame em uma aba separada
            df_tab1.to_excel(writer, sheet_name='registros', index=False)
            df_tab2.to_excel(writer, sheet_name='dicionario', index=False)
            df_tab3.to_excel(writer, sheet_name='enfermidades', index=False)

        return path
