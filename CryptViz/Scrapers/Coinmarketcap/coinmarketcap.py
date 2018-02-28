import requests
from lxml import etree
import pandas as pd
import os
import urllib.parse

class CoinMarketcap():

    def __init__(self):
        self.root_url = "http://coinmarketcap.com"
        self.dir = os.path.dirname(__file__) + "/data/"
        self.tree = self.read()

    def get(self):
        """
        Requests coinmarketcap.com and saves results to disk.
        """
        cmc = requests.get(self.root_url)
        text = cmc.text
        with open(os.path.join(self.dir,'coinmarketcap.html'), 'w+',encoding="utf8") as f:
            f.write(text)
        return text

    def read(self):
        """
        Returns an lxml etree of coinmarketcap.html.
        Uses cached version if exists, otherwise calls get().
        """
        try:
            with open(os.path.join(self.dir,'coinmarketcap.html'),encoding="utf8") as f:
                text = f.read()
        except FileNotFoundError:
            print(FileNotFoundError)
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
        "Returns a list of Coin objects."
        coins = zip(self.coin_names(), self.coin_urls())
        coins = [Coin(name, url) for (name, url) in coins]
        return coins

    def all_coin_data(self, ret_df=True, ret_json=False, github=False):
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
        if ret_json:
            return all_coin_data
        if ret_df:
            return pd.DataFrame(all_coin_data)

class Scraper():
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.dir = os.path.dirname(__file__) + "/data/"
        self.tree = self.read()

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.json())

    def get(self):
        """
        Get's the page http://github.com/relative_url
        """
        page = requests.get(self.url)
        text = page.text
        with open(os.path.join(self.dir,'{}.html'.format(self.name)), 'w+',encoding="utf8") as f:
            f.write(text)
        return text

    def read(self):
        try:
            with open(os.path.join(self.dir,'{}.html'.format(self.name)),encoding="utf8") as f:
                text = f.read()
        except FileNotFoundError:
            print(FileNotFoundError)
            text = self.get()
        tree = etree.HTML(text)
        self.tree = tree
        return tree

    def json(self):
        return """Overwride this function!"""


class GitHub(Scraper):
    def __init__(self, name, url, coin):
        super().__init__(name, url)
        self.coin = coin

    def json(self):
        github_data = {
                'name': self.name,
                'url': self.url,
                }
        return github_data

    def pinned_repos(self):
        pinned_repos = self.tree.findall(".//div[@class='pinned-repo-item-content']") 
        repos = []
        for e in pinned_repos:
                name = e.find(".//span[@class='repo js-repo']").text
                url = urllib.parse.urljoin(self.url, e          \
                        .find(".//span[@class='repo js-repo']") \
                        .getparent()    \
                        .attrib['href'])
                description = e.find(".//p").text
                repo = Repo(name+"-repo", url, description)
                repos.append(repo)
        return repos


class Repo(Scraper):
    def __init__(self, name, url, description):
        super().__init__(name, url)
        self.description = description

    def json(self):
        repo_data = {
                'name': self.name,
                'url': self.url,
                'description': self.description,
                'language': self.language(),
                'stars': self.stars(),
                'forks': self.forks(),
                'watch': self.watch(),
                }
        return repo_data

    def language(self):
        langs = self.tree.findall(".//span[@class='lang']")
        langs = [l.text for l in langs]
        return langs[0]

    def stars(self):
        stars = self.tree.find(".//a[@class='social-count js-social-count']") 
        stars = stars.text.strip()
        return int(stars.replace(',',''))

    def forks(self):
        links = self.tree.findall(".//a") 
        forks = [a for a in links if a.attrib['href'].endswith('network')][0]
        forks = forks.text.strip()
        return int(forks.replace(',',''))

    def watch(self):
        links = self.tree.findall(".//a") 
        watch = [a for a in links if a.attrib['href'].endswith('watchers')][0]
        watch = watch.text.strip()
        return int(watch.replace(',',''))

class Coin(Scraper):
    def __init__(self, name, relative_url):
        url = "http://coinmarketcap.com" + relative_url
        super().__init__(name, url)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.json())

    def json(self):
        coin_data = {
                'name': self.name,
                'url': self.url,
                'symbol': self.symbol(),
                'price': self.price(),
                'volume': self.volume(),
                'marketcap': self.marketcap(),
                'timestamp': None,
                'github_url': self.github_url(),
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

    def github_url(self):
        links = self.tree.findall(".//a")
        try:
            github_url = [l.attrib['href'] for l in links if l.text == "Source Code"][0]
        except IndexError:
            github_url = None
        return github_url

    def forum_url(self):
        links = self.tree.findall(".//a")
        github_url = [l.attrib['href'] for l in links if l.text == "Source Code"][0]
        return github_url

    def github(self):
        return GitHub(name=self.name + "-github", url=self.github_url(), coin=self.name)

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
        return int(today['Market Cap'][0])

    def read_history(self):
        try:
            df = pd.read_csv(os.path.join(self.dir,'{}-history.csv'.format(self.name)))
        except FileNotFoundError:
            print(FileNotFoundError)
            df = self.get_history()
        return df

    def get_history(self):
        url = self.url + "/historical-data"
        df = pd.read_html(url)[0]
        df.to_csv(os.path.join(self.dir,'{}-history.csv'.format(self.name)))
        return df

