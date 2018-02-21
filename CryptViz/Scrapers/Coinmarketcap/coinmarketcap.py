import requests
from lxml import etree
import pandas as pd
import os

class CoinMarketcap():

    def __init__(self):
        self.root_url = "http://coinmarketcap.com"
        self.dir = os.path.dirname(__file__) + "/data/"
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

    def all_coin_data(self, return_json=False):
        """
        Generate a list of coin objects, containing all fields as specified in
        the Coin class.
        """
        all_coin_data = []
        coins = self.coins()
        for coin in coins:
            coin = self.coin(coin)
            coin_data = coin.all_fields()
            all_coin_data.append(coin_data)
        if return_json:
            return all_coin_data
        else:
            return pd.DataFrame(all_coin_data)




class Coin():
    def __init__(self, name, relative_url):
        self.url = "http://coinmarketcap.com" + relative_url
        self.dir = os.path.dirname(__file__) + "/data/"
        self.name = name
        self.tree = self.read()

    def __str__(self):
        return self.name

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

    def all_fields(self):
        coin_data = {
                'name': self.name,
                'url': self.url,
                'symbol': self.symbol(),
                'price': self.price(),
                'volume': self.volume(),
                'marketcap': self.marketcap(),
                }
        return coin_data

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

    def today(self):
        history = self.read_history()
        today = history.head(1)
        return today

    def price(self):
        today = self.today()
        return today['Open'][0]

    def volume(self):
        today = self.today()
        return today['Volume'][0]

    def marketcap(self):
        today = self.today()
        return today['Market Cap'][0]

    def read_history(self):
        try:
            df = pd.read_csv(os.path.join(self.dir,'{}-history.csv'.format(self.name)))
        except FileNotFoundError:
            df = self.get_history()
        return df

    def get_history(self):
        url = self.url + "/historical-data"
        df = pd.read_html(url)[0]
        df.to_csv(os.path.join(self.dir,'{}-history.csv'.format(self.name)))
        return df

