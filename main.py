import src.loaders as loaders
import src.processing as processing


convenio = loaders.DataLoader.load_data('data/cobrancas_convenio.csv')
internas = loaders.DataLoader.load_data('data/cobrancas_internas.xlsx')

convenio['nome_beneficiario'] = convenio['nome_beneficiario'].apply(processing.Processing.normalize_name)
internas['paciente'] = internas['paciente'].apply(processing.Processing.normalize_name)

print(convenio.head())

print(internas.head())

