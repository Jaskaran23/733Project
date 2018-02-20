import requests

class pageScraper():
    def __init__(api_url):
        self.api_url = api_url

    def get_page(url):
    def exract_json(page):
    def post_json(data):
        requests.post(self.api_url, data)


class coinCrawler(pageScraper):
    def __init__(api_url='/api/pages'):
        self.api_url = api_url
        self.link_heap = default_dict(list)

    def crawl(url='https://coinmarketcap.com/'):
        while(True):
            # Get page, extract data to json, post json to API
            page = self.get_page(url)
            data_object = self.extract_json(page)
            self.post_json(data_object) 

            out_links = data_object['out_links']
            for link in out_links:
                # If this link has been explored, don't go
                # Add link to rank of explored site
                self.add_to_queue(lin


        

class coinMarketCapScraper():
    def get_100_coins
    def get_coin_page(coin)
