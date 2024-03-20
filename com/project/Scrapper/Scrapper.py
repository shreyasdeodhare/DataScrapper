from zenrows import ZenRowsClient
import csv
from bs4 import BeautifulSoup

def fetch_html_content(url):
    client = ZenRowsClient("175281317b5eae9f6a7af570a946513d6df7fdf4")
    response = client.get(url)
    return response.text

def scrape_and_save_csv(html_content, csv_path):
    soup = BeautifulSoup(html_content, 'html.parser')
    div_elements = soup.find_all("div")
    
    unique_entries = set()
    
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file: 
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["DivIndex", "TagName", "TagContent"])
        
        for i, div in enumerate(div_elements): 
            for j, tag in enumerate(div.find_all()):
                tag_name = tag.name if tag.name else 'Text'
                tag_content = ' '.join(tag.strings)
                
                if tag_content not in unique_entries:
                    csv_writer.writerow([i+1, tag_name, tag_content])
                    unique_entries.add(tag_content)

url = "https://www.linkedin.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
csv_path = "D:\\DataScrapper\\com\\project\\Scrapper\\data1.csv"

html_content = fetch_html_content(url)
scrape_and_save_csv(html_content, csv_path)
