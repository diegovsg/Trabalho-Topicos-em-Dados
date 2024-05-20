import pandas as pd
from IPython.display import display
from pandasgui import show


# df = pd.read_csv(r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue24_mes.csv', encoding='cp1252')

# df.to_excel(r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue24_mes.xlsx', index=False)

# Ler o arquivo Excel
df = pd.read_excel(r'C:\Users\Diego\Documents\GitHub\Trabalho-Topicos-em-Dados\downloads\dengue24_mes.xlsx')

# Visualizar as primeiras linhas do DataFrame
print(df.head())

# Informações gerais sobre o DataFrame
print("\nInformações gerais do DataFrame:")
print(df.info())

# Estatísticas descritivas
print("\nEstatísticas descritivas do DataFrame:")
print(df.describe())

# Verificando se há valores nulos
print("\nValores nulos no DataFrame:")
print(df.isnull().sum())

# Visualizar o DataFrame como uma tabela
display(df)

# Abrir a interface gráfica do pandasgui
show(df)
