import requests
from bs4 import BeautifulSoup
import time


def scrape(_url):
    
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    mcaps = soup.find_all('td', class_="td-market_cap cap col-market cap-price text-right")
    tickers = soup.find_all(attrs={'class':"d-lg-inline font-normal text-3xs tw-ml-0 md:tw-ml-2 md:tw-self-center tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60"})
    output = open('./output/testrun2.txt','a')
    for i in range(len(mcaps)):
        mcapInteger = int(mcaps[i].contents[1].string.replace(',','').replace('$',''))
        if mcapInteger < 5000000 and mcapInteger > 250000:
            output.write(f"\n\nTicker: {tickers[i].string}")
            output.write(f"Market Cap: \n{mcaps[i].contents[1].string}")
    output.close()



for i in range(1,100):
    print(f"Scraping page {i}...")
    url = f'https://www.coingecko.com/?page={i}'
    scrape(url)
    print(f"Page {i} complete. \n")
    time.sleep(3)