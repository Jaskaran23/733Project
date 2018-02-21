import requests
from lxml import etree
import pandas as pd
import os

class CoinMarketcap():

    def __init__(self):
        self.root_url = "http://coinmarketcap.com"
        self.dir = os.path.dirname(__file__)
        self.tree = self.read()

    def get(self):
        cmc = requests.get(self.root_url)
        text = cmc.text
        with open(os.path.join(self.dir,'coinmarketcap.html'), 'w+') as f:
            f.write(text)
        return text

    def read(self):
        try:
            with open(os.path.join(self.dir,'coinmarketcap.html')) as f:
                text = f.read()
        except FileNotFoundError:
            text = self.get()
        tree = etree.HTML(text)
        return tree

    def coin_names(self):
        """ 
        Returns a list the 100 coins from the front page of coinmarketcap.com
        """
        coins = self.tree.findall(".//a[@class='currency-name-container']") 
        coin_names = [e.text for e in coins]
        return coin_names

    def coin_urls(self):
        """ 
        Returns a list of 100 URLs. The ith URL is a the relative path for the 
        coinmarketcap page corresponding to the ith coin from coinmarketcap. 
        """
        coins = self.tree.findall(".//a[@class='currency-name-container']") 
        coin_urls = [e.attrib['href'] for e in coins]
        return coin_urls

    def coins(self):
        "Returns a list of dicts representing coins."
        cn = self.coin_names()
        cu = self.coin_urls()
        coins = [{'name':x[0],'relative_url':x[1]} for x in zip(cn,cu)]
        return coins

    def coin(self, coin):
        """
        Takes a dict representing a coin. Returns a coin object representing that
        coin's page on coinmarketcap.com.
        """
        return Coin(coin['name'], coin['relative_url'])

class Coin():
    def __init__(self, name, relative_url):
        self.url = "http://coinmarketcap.com" + relative_url
        self.dir = os.path.dirname(__file__)
        self.name = name
        self.tree = self.read()

    def get(self):
        """
        Get's the page http://coinmarketcap.com/currencies/coin
        """
        page = requests.get(self.url)
        text = page.text
        with open(os.path.join(self.dir,'{}.html'.format(self.name)), 'w+') as f:
            f.write(text)
        return text

    def read(self):
        try:
            with open(os.path.join(self.dir,'{}.html'.format(self.name))) as f:
                text = f.read()
        except FileNotFoundError:
            text = self.get()
        tree = etree.HTML(text)
        return tree

    def symbol(self):
        symbol = self.tree.find(".//small[@class='bold hidden-xs']") 
        # Strip Parenthesis
        symbol = symbol.text[1:-1]
        return symbol

    def website(self):
        links = self.tree.findall(".//a")
        website = [l.attrib['href'] for l in links if l.text == "Website"][0]
        return website

    def github(self):
        links = self.tree.findall(".//a")
        github = [l.attrib['href'] for l in links if l.text == "Source Code"][0]

    def history(self):
        url = self.url + "/historical-data"
        df = pd.read_html(url)[0]
        return df

