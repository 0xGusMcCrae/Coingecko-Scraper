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

            #go into token's individual page to find twitter, get twitter join date and follower count
            tokenName = tokenName.lower().replace(' ','-')
            tokenUrl = f'https://www.coingecko.com/en/coins/{tokenName}'
            print('\n' + tokenUrl)

            tokenPage = requests.get(tokenUrl)
            tokenSoup = BeautifulSoup(tokenPage.content,'html.parser')
            try:
                twitterUrl = tokenSoup.find('i', class_="fab mr-1 fa-twitter").parent.get('href')
                print(twitterUrl)
            except:
                twitterUrl = None
            if twitterUrl is not None:
                twitterPage = requests.get(twitterUrl)
                twitterSoup = BeautifulSoup(twitterPage.content,'html.parser')
                twitterJoinDate = twitterSoup.find('span',class_="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0").string
                print(twitterJoinDate)
                # output.write(f"\nTwitter Join Date: {twitterJoinDate}")
    output.close()

 #need to figure out how to wait until javascript is done running to get the html
 #or how to get twitter not to return Something went wrong, but don’t fret — let’s give it another shot.


for i in range(12,13):
    print(f"Scraping page {i}...")
    url = f'https://www.coingecko.com/?page={i}'
    scrape(url)
    print(f"Page {i} complete. \n")
    time.sleep(1)