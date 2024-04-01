import requests
from bs4 import BeautifulSoup

def scrape_dengue_data():
    url = "https://saude.sp.gov.br/cve-centro-de-vigilancia-epidemiologica-prof.-alexandre-vranjac/oldzoonoses/dengue/dados-estatisticos"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the link to the page containing the data for 2024
        link_2024 = soup.find('a', string='2024 por mês  e  semana epidemiológica  (html)')
        
        if link_2024:
            data_url_2024 = link_2024.get('href')
            data_response_2024 = requests.get(data_url_2024)
            
            if data_response_2024.status_code == 200:
                data_soup_2024 = BeautifulSoup(data_response_2024.content, 'html.parser')
                
                # Find all links for each month
                month_links = data_soup_2024.find_all('a', href=True)
                
                for month_link in month_links:
                    month_url = month_link['href']
                    month_response = requests.get(month_url)
                    
                    if month_response.status_code == 200:
                        month_soup = BeautifulSoup(month_response.content, 'html.parser')
                        
                        # Assuming the table is the only one on the page, you can find it like this
                        table = month_soup.find('table')
                        
                        if table:
                            # Process the table data as needed
                            for row in table.find_all('tr'):
                                cells = row.find_all('td')
                                if cells:
                                    # Example: print the text content of each cell
                                    row_data = [cell.get_text(strip=True) for cell in cells]
                                    print(row_data)
                        else:
                            print("No table found on the month page:", month_url)
                    else:
                        print("Failed to retrieve month page:", month_url)
            else:
                print("Failed to retrieve 2024 data page.")
        else:
            print("Link to 2024 data page not found.")
    else:
        print("Failed to retrieve main page.")

if __name__ == "__main__":
    scrape_dengue_data()
