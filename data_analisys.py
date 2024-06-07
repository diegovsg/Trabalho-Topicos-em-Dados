import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate


def modificar_coluna_tabela(file_path):
    # Carregar o arquivo CSV
    dengue_data = pd.read_csv(file_path)

    # Separar a coluna 'Município' em 'id_municipio' e 'nome_municipio'
    dengue_data[['id_municipio', 'nome_municipio']] = dengue_data['Município'].str.extract(r'(\d+)\s+(.+)')
    dengue_data = dengue_data.drop(columns=['Município'])

    # Converter colunas numéricas para inteiros, ignorando erros
    numeric_columns = dengue_data.columns[3:-2]  # Ignora as primeiras colunas e as últimas duas ('Total Notificados' e 'Total Confirmados')
    for column in numeric_columns:
        if dengue_data[column].dtype == 'object':
            dengue_data[column] = pd.to_numeric(dengue_data[column].str.replace(',', ''), errors='coerce').fillna(0).astype(int)
        else:
            dengue_data[column] = dengue_data[column].fillna(0).astype(int)

    # Verificar as primeiras linhas para assegurar a separação correta
    print(tabulate(dengue_data[['id_municipio', 'nome_municipio']].head(), headers='keys', tablefmt='psql'))

    return dengue_data

def criarArquivoAtualizado(file_path, new_file_path):
    arquivo_modificado = modificar_coluna_tabela(file_path)

    # Salvar o dataframe atualizado de volta para um arquivo CSV, com um novo nome para comparação
    arquivo_modificado.to_csv(new_file_path, index=False)

    # Carregar o arquivo CSV atualizado
    dengue_data_atualizado = pd.read_csv(new_file_path)

    print(tabulate(dengue_data_atualizado.head(), headers='keys', tablefmt='psql'))

def analisar_dados_dengue(file_path):
    # Carregar o arquivo CSV
    dengue_data = pd.read_csv(file_path)

    # Extrair os nomes dos meses das colunas (excluindo as colunas iniciais e finais não relacionadas aos meses)
    meses = dengue_data.columns[3:-2]  # Ignora as primeiras colunas e as últimas duas ('Total Notificados' e 'Total Confirmados')

    # Criar um dicionário para armazenar os totais de casos confirmados e notificados por mês
    totals_by_month = {}

    # Iterar sobre os nomes dos meses
    for mes in meses:
        # Separar o nome do mês e o tipo de caso (confirmado ou notificado)
        nome_mes, tipo_caso = mes.rsplit(' ', 1)

        # Se não existir um dicionário para o mês, crie um
        if nome_mes not in totals_by_month:
            totals_by_month[nome_mes] = {'Confirmados': 0, 'Notificados': 0}

        # Adicionar os valores de casos confirmados ou notificados ao total do mês
        if dengue_data[mes].dtype == 'object':
            totals_by_month[nome_mes][tipo_caso] += pd.to_numeric(dengue_data[mes].str.replace(',', ''), errors='coerce').fillna(0).astype(int).sum()
        else:
            totals_by_month[nome_mes][tipo_caso] += dengue_data[mes].fillna(0).astype(int).sum()

    return pd.DataFrame(totals_by_month).transpose()  # Transformar o dicionário em DataFrame e transpor para ter meses como índice

def criar_graficos(analise_result):
    plt.figure(figsize=(14, 8))
    
    # Gráfico de casos notificados e confirmados
    sns.lineplot(data=analise_result, markers=True)
    plt.title('Casos Notificados e Confirmados por Mês')
    plt.xlabel('Meses')
    plt.ylabel('Número de Casos')
    plt.legend(['Notificados', 'Confirmados'])
    plt.grid(True)
    plt.show()
    
# Caminho para os arquivos
file_path = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue22_mes.csv'
new_file_path = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue22_mes_atualizado.csv'

# Modificar e salvar o arquivo atualizado
criarArquivoAtualizado(file_path, new_file_path)

# Analisar os dados do arquivo atualizado
analise_result = analisar_dados_dengue(new_file_path)
print(analise_result)

# Criar gráficos com os resultados da análise
criar_graficos(analise_result)