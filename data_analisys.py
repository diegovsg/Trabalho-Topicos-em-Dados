import pandas as pd
from tabulate import tabulate

def modificar_coluna_tabela():
    # Usar uma das abordagens para corrigir o caminho do arquivo
    file_path = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue22_mes.csv'

    # Carregar o arquivo CSV
    dengue_data = pd.read_csv(file_path)

    # Separar a coluna 'Município' em 'id_municipio' e 'nome_municipio'
    dengue_data[['id_municipio', 'nome_municipio']] = dengue_data['Município'].str.split(' ', n=1, expand=True)

    # Verificar as primeiras linhas para assegurar a separação correta
    print(tabulate(dengue_data[['Município', 'id_municipio', 'nome_municipio']].head(), headers='keys', tablefmt='psql'))

    return dengue_data

def criarArquivoAtualizado(arquivo_modificado):
    arquivo_modificado = modificar_coluna_tabela()

    # Defina o número máximo de linhas e colunas a serem exibidas
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Salvar o dataframe atualizado de volta para um arquivo CSV, com um novo nome para comparação
    new_file_path = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue22_mes_atualizado.csv'
    arquivo_modificado.to_csv(new_file_path, index=False)

    # Carregar o arquivo CSV
    dengue_data_atualizado = pd.read_csv(new_file_path)

    print(tabulate(dengue_data_atualizado, headers='keys', tablefmt='psql'))

def analisar_dados_dengue(file_path):
    # Carregar o arquivo CSV
    dengue_data = pd.read_csv(file_path)

    # Extrair os nomes dos meses das colunas
    meses = dengue_data.columns[1:]  # Ignora a primeira coluna que contém os municípios

    # Criar um dicionário para armazenar os totais de casos confirmados e notificados por mês
    totals_by_month = {}

    # Iterar sobre os nomes dos meses
    for mes in meses:
        # Separar o nome do mês e o tipo de caso (confirmado ou notificado)
        nome_mes, tipo_caso = mes.split(' ')

        # Se não existir um dicionário para o mês, crie um
        if nome_mes not in totals_by_month:
            totals_by_month[nome_mes] = {'Confirmados': 0, 'Notificados': 0}

        # Adicionar os valores de casos confirmados ou notificados ao total do mês
        totals_by_month[nome_mes][tipo_caso] += dengue_data[mes].sum()

    return pd.DataFrame(totals_by_month).transpose()  # Transformar o dicionário em DataFrame e transpor para ter meses como índice

file_path = r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue_data_atualizado.csv'
analise_result = analisar_dados_dengue(file_path)
print(analise_result)

