import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import seaborn as sns


# Função para modificar a tabela
def modificar_coluna_tabela(file_path):
    dengue_data = pd.read_csv(file_path)
    dengue_data[['id_municipio', 'nome_municipio']] = dengue_data['Município'].str.extract(r'(\d+)\s+(.+)')
    dengue_data = dengue_data.drop(columns=['Município'])
    numeric_columns = dengue_data.columns[3:-2]
    for column in numeric_columns:
        if dengue_data[column].dtype == 'object':
            dengue_data[column] = pd.to_numeric(dengue_data[column].str.replace(',', ''), errors='coerce').fillna(0).astype(int)
        else:
            dengue_data[column] = dengue_data[column].fillna(0).astype(int)
    print(tabulate(dengue_data[['id_municipio', 'nome_municipio']].head(), headers='keys', tablefmt='psql'))
    return dengue_data

# Função para criar arquivo atualizado
def criarArquivoAtualizado(file_path, new_file_path):
    arquivo_modificado = modificar_coluna_tabela(file_path)
    arquivo_modificado.to_csv(new_file_path, index=False)
    dengue_data_atualizado = pd.read_csv(new_file_path)
    print(tabulate(dengue_data_atualizado.head(), headers='keys', tablefmt='psql'))

# Função para analisar dados de dengue
def analisar_dados_dengue(file_path):
    dengue_data = pd.read_csv(file_path)
    meses = dengue_data.columns[3:-2]
    totals_by_month = {}
    for mes in meses:
        nome_mes, tipo_caso = mes.rsplit(' ', 1)
        if nome_mes not in totals_by_month:
            totals_by_month[nome_mes] = {'Confirmados': 0, 'Notificados': 0}
        if dengue_data[mes].dtype == 'object':
            totals_by_month[nome_mes][tipo_caso] += pd.to_numeric(dengue_data[mes].str.replace(',', ''), errors='coerce').fillna(0).astype(int).sum()
        else:
            totals_by_month[nome_mes][tipo_caso] += dengue_data[mes].fillna(0).astype(int).sum()
    return pd.DataFrame(totals_by_month).transpose()

# Função para criar gráficos
def criar_graficos(analise_result):
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=analise_result, markers=True)
    plt.title('Casos Notificados e Confirmados por Mês')
    plt.xlabel('Meses')
    plt.ylabel('Número de Casos')
    plt.legend(['Notificados', 'Confirmados'])
    plt.grid(True)
    plt.show()

# Caminhos para os arquivos de 2024 e 2023
file_path_2024 = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue23_mes.csv'
new_file_path_2024 = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue23_mes_atualizado.csv'
file_path_2023 = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue22_mes.csv'
new_file_path_2023 = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue22_mes_atualizado.csv'

# Processar e analisar dados de 2024
criarArquivoAtualizado(file_path_2024, new_file_path_2024)
analise_result_2024 = analisar_dados_dengue(new_file_path_2024)

# Processar e analisar dados de 2023
criarArquivoAtualizado(file_path_2023, new_file_path_2023)
analise_result_2023 = analisar_dados_dengue(new_file_path_2023)

# Comparar os dados de 2024 com 2023
combined_data = pd.concat([analise_result_2024, analise_result_2023], keys=['2022', '2023'], names=['Ano', 'Mes'])

# Criar gráficos comparativos
def criar_graficos_comparativos(combined_data):
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=combined_data.reset_index(), x='Mes', y='Confirmados', hue='Ano', style='Ano', markers=True, dashes=False)
    plt.title('Casos Confirmados por Mês (2023 vs 2022)')
    plt.xlabel('Meses')
    plt.ylabel('Número de Casos Confirmados')
    plt.grid(True)
    plt.show()
    
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=combined_data.reset_index(), x='Mes', y='Notificados', hue='Ano', style='Ano', markers=True, dashes=False)
    plt.title('Casos Notificados por Mês (2023 vs 2022)')
    plt.xlabel('Meses')
    plt.ylabel('Número de Casos Notificados')
    plt.grid(True)
    plt.show()

# Criar gráficos comparativos
criar_graficos_comparativos(combined_data)
