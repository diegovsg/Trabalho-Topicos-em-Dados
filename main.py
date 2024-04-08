import requests
from bs4 import BeautifulSoup


def scrape_dengue_data():
    url = "https://saude.sp.gov.br/cve-centro-de-vigilancia-epidemiologica-prof.-alexandre-vranjac/oldzoonoses/dengue/dados-estatisticos"
    response = requests.get(url)
    lista_links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Encontre todos os links dentro do elemento com a classe "publish"
        links = soup.select('.publish a[href]')
        
        # Iterar sobre os links e imprimir seus URLs
        for link in links:
            print("Salvando na lista:", link['href'])
            lista_links = link['href']

    return lista_links


def scrapeTabela(links_encontrados):
    #falta saber que é de 2024 !!
    for links in links_encontrados:
        print(links)
        url_2024 = links

    # Fazer uma solicitação HTTP para o URL
    link_response = requests.get(url_2024)
            
    # Verificar se a solicitação foi bem-sucedida
    if link_response.status_code == 200:
        soup = BeautifulSoup(link_response.content, 'html.parser')
        link_url = soup.select('.publish a[href]')
        print("Conteúdo da página acessada")
        scrapeTabela(link_response)
    else:
        print("Falha ao acessar:", link_url)
   
    print(soup)
    

if __name__ == "__main__":
    links_encontrados = scrape_dengue_data()
    scrapeTabela(links_encontrados)
