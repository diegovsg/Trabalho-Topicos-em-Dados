import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin



def scrape_dengue_data():
    url = "https://saude.sp.gov.br/cve-centro-de-vigilancia-epidemiologica-prof.-alexandre-vranjac/oldzoonoses/dengue/dados-estatisticos"
    response = requests.get(url)
    lista_links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Encontre todos os links dentro do elemento com a classe "publish"
        links = soup.select('.publish a[href]')
        
        # Itera sobre os links e verifica se contêm "2022", "2023" ou "2024" no atributo href
        for link in links:
            href = link.get('href')
            if href and re.search(r'/(2022|2023|2024)/', href):
                lista_links.append(href)

    print(lista_links)
    return lista_links

def download(links):
    # URL base do site
    base_url = "https://saude.sp.gov.br"

    # Criar uma pasta para salvar os arquivos, se não existir
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    for link in links:
        full_url = urljoin(base_url, link)  # Concatenar o link extraído com o URL base
        filename = link.split('/')[-1]  # Extrair o nome do arquivo do URL
        filepath = os.path.join('downloads', filename)  # Caminho completo para salvar o arquivo
        # Fazer o download do conteúdo do link
        response = requests.get(full_url)
        if response.status_code == 200:
            # Salvar o conteúdo do link no arquivo
            with open(filepath, 'wb') as f:
                f.write(response.content)
                print(f"Arquivo '{filename}' baixado com sucesso.")
        else:
            print(f"Falha ao baixar o arquivo '{filename}'.")

# Obter os links de todos os anos
links = scrape_dengue_data()

# Baixar os arquivos
download(links)

if __name__ == "__main__":
    # Obter os links de todos os anos
    links_encontrados = scrape_dengue_data()

    # Baixar os arquivos
    download(links_encontrados)
