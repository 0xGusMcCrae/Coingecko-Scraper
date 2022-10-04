import requests
from bs4 import BeautifulSoup
import time


def scrape(_url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    mcaps = soup.find_all('td', class_="td-market_cap cap col-market cap-price text-right")
    tickers = soup.find_all(attrs={'class':"d-lg-inline font-normal text-3xs tw-ml-0 md:tw-ml-2 md:tw-self-center tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60"})
    tokenNames = soup.find_all('span', class_="lg:tw-flex font-bold tw-items-center tw-justify-between")
    output = open('./output/testrun2.txt','a')
    for i in range(len(mcaps)):
        mcapInteger = int(mcaps[i].contents[1].string.replace(',','').replace('$',''))
        if mcapInteger < 5000000 and mcapInteger > 250000:
            tokenName = tokenNames[i].string.replace('\n','')
            ticker = tickers[i].string.replace('\n','')
            marketCap = mcaps[i].contents[1].string
            output.write(f"\n\nToken: {tokenName}")
            output.write(f"\nTicker: {ticker}")
            output.write(f"\nMarket Cap: {marketCap}")
            #go into token's individual page to find release date
            tokenName = tokenName.lower().replace(' ','-')
            tokenUrl = f'https://www.coingecko.com/en/coins/{tokenName}'
            tokenSocialUrl = tokenUrl + '#social'
            print(f'\n{tokenSocialUrl}')
            tokenPage = requests.get(tokenUrl,timeout=None)
            time.sleep(1)
            tokenSocialPage = requests.get(tokenSocialUrl,timeout=None)
            time.sleep(1)
            tokenSoup = BeautifulSoup(tokenPage.content,'html.parser')
            tokenSocialSoup = BeautifulSoup(tokenSocialPage.content,'html.parser')
            # for item in tokenSocialSoup:
            #     output.write(str(item))
            launchDate = tokenSoup.find_all('g', class_="highcharts-label highcharts-range-input")
            output.write(f"\nDate Added to Coingecko: {launchDate}")
            twitterFollowers = tokenSocialSoup.find_all('div', class_="mt-4 mb-2 text-2xl")
            output.write(f"\nTwitter Followers: {twitterFollowers}")
    output.close()

 #need to figure out how to wait until javascript is done running to get the html


for i in range(12,13):
    print(f"Scraping page {i}...")
    url = f'https://www.coingecko.com/?page={i}'
    scrape(url)
    print(f"Page {i} complete. \n")
    time.sleep(1)