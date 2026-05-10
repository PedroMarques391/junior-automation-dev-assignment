from pathlib import Path

import pandas as pd


class Reporter:
    def __init__(self, df_data: pd.DataFrame, output_folder: str):
        self.df_data = df_data
        self.output_folder = output_folder
        
    def _generate_summary(self) -> pd.DataFrame:
        total_pdf_renamed = 0
        
        for file in Path("/data/laudos_renomeados").glob('*.pdf'):
            total_pdf_renamed += 1
        
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
                self.df_data['vl_liquido'].sum(),
                self.df_data['vl_glosa'].sum(),
                total_pdf_renamed 
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

        