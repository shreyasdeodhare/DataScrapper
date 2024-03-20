import requests
from bs4 import BeautifulSoup
import concurrent.futures
import csv

# Get the list of free proxies
def getProxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text == 'elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies

def extract(proxy):
    try:
        r = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
        status_code = r.status_code
        response = r.json()
        # Write only the IP address of the valid proxy to the CSV file
        if status_code == 200:
            with open('proxies.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([proxy.split(':')[0]])  # Write only the IP address
    except requests.ConnectionError as err:
        pass  # Ignore connection errors
    return proxy

proxylist = getProxies()

# Check them all with ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(extract, proxylist)
