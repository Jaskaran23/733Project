import requests
from lxml import etree
import pandas as pd
import os

root_url = "http://coinmarketcap.com"
dir = os.path.dirname(__file__)

def cache_coinmarketcap():
    cmc = requests.get(root_url)
    text = cmc.text
    with open(os.path.join(dir,'coinmarketcap.html'), 'w+') as f:
        f.write(text)

def read_coinmarketcap():
    with open(os.path.join(dir,'coinmarketcap.html')) as f:
        text = f.read()
    tree = etree.HTML(text)

    coins = tree.findall(".//a[@class='currency-name-container']") 
    coin_names = [e.text for e in coins]
    print(coins)
    coin_urls = [e.attrib['href'] for e in coins]
    print(coin_urls)

def cache_coin(coin, coin_url):
    url = root_url + coin_url
    coin_page = requests.get(url)
    text = coin_page.text
    with open(os.path.join(dir,'{}.html'.format(coin)), 'w+') as f:
        f.write(text)

def read_coin(coin):
    with open(os.path.join(dir,'{}.html'.format(coin))) as f:
        text = f.read()
    tree = etree.HTML(text)

    token_symbol = tree.find(".//small[@class='bold hidden-xs']") 
    # Strip Parenthesis
    token_symbol = token_symbol.text[1:-1]

def get_coin_history(coin_url):
    url = root_url + coin_url + "/historical-data"
    df = pd.read_html(url)[0]


def coin_name_to_url(coin):
    coin = coin.lower().replace(" ", "-")
    return coin

