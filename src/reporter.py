from datetime import datetime
from pathlib import Path

import openpyxl as opxl
import pandas as pd

from src.processing import Processing


class Reporter:
    def __init__(self, df_data: pd.DataFrame, output_folder: str):
        self.df_data = df_data
        self.output_folder = output_folder
        
    def _generate_summary(self) -> pd.DataFrame:
        
        summary_data = {
            "Descrição": [
                "Total de Cobranças (Interno)",
                "Total de Cobranças (CSV)",
                "Valor Líquido Total (CSV)",
                "Total de Glosas",
                "Laudos Renomeados com Sucesso"
            ],
            "Valor": [ 
                len(self.df_data[self.df_data['_merge'] != 'right_only']),
                len(self.df_data[self.df_data['_merge'] != 'left_only']),
                self.df_data['vl_liquido'].apply(Processing.normalize_value_csv_to_float).sum(),
                self.df_data['vl_glosa'].apply(Processing.normalize_value_csv_to_float).sum(),
                self.df_data['arquivo_renomeado'].count()
            ]
        }
        return pd.DataFrame(summary_data)

    def _generate_detailed_data(self) -> pd.DataFrame:
        detailed_data = {
            "Detalhes": [
                "ID Cobrança",
                "Procedimento",
                "CPF Beneficiário",
                "Código TUSS",
                "Nome Operadora",
                "PDF Renomeado",
                "Divergencias"
            ],
            "Dados": [
                self.df_data['num_guia'],
                self.df_data['procedimento'],
                self.df_data['cpf_beneficiario'],
                self.df_data['cod_tuss'],
                self.df_data['nome_operadora'],
                self.df_data['arquivo_renomeado'],
                self.df_data['divergencias']
            ]
        }
        return pd.DataFrame(detailed_data)
    
    def _generate_alerts(self) -> pd.DataFrame:
        
      df_alerts = self.df_data[self.df_data['divergencias'].notna() & (self.df_data['divergencias'] != "Ok")]
      
      return df_alerts

    def generate_report(self) -> None:
        summary_df = self._generate_summary()
        detailed_df = self._generate_detailed_data()
        alerts_df = self._generate_alerts()
        
        wb = opxl.Workbook()
        ws_summary = wb.active
        ws_summary.title = "Resumo"
        headers = summary_df.columns.tolist()
        ws_summary.append(headers)
        for row in summary_df.itertuples(index=False):
            ws_summary.append(row)
        
        path_name = f"relatorio_faturamento_{datetime.now().strftime('%Y-%m')}.xlsx"
        
        Path(self.output_folder).mkdir(parents=True, exist_ok=True)
        wb.save(self.output_folder + '/' + path_name)
        
         

        