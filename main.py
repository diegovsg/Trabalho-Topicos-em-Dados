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
        
        # # Iterar sobre os links e imprimir seus URLs
        # for link in links:
        #     #print("Salvando na lista:", link['href'])
        #     lista_links = link['href']
        # Itera sobre os links e verifica se contêm "2024" no atributo href
        for link in links:
            href = link.get('href')
            if href and re.search(r'/2024/', href):
                lista_links.append(href)

    print(lista_links)
    return lista_links

def download(links_2024):
    # URL base do site
    base_url = "https://saude.sp.gov.br"

    # Criar uma pasta para salvar os arquivos, se não existir
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    for link in links_2024:
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
        

# def scrapeTabela(links_encontrados):
#     #falta saber que é de 2024 !!
#     for links in links_encontrados:
#         print(links)
#         url_2024 = links

#     # Fazer uma solicitação HTTP para o URL
#     link_response = requests.get(url_2024)
            
#     # Verificar se a solicitação foi bem-sucedida
#     if link_response.status_code == 200:
#         soup = BeautifulSoup(link_response.content, 'html.parser')
#         link_url = soup.select('.publish a[href]')
#         print("Conteúdo da página acessada")
#         scrapeTabela(link_response)
#     else:
#         print("Falha ao acessar:", link_url)
   
#     print(soup)
    

if __name__ == "__main__":
    links_encontrados = scrape_dengue_data()
    download(links_encontrados)

