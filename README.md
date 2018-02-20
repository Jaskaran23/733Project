# Big Data II Final Project: CryptViz
Can we visualize the cryptocurrency ecosystem?

### About
Information can be found here in the [project proposal](https://docs.google.com/document/d/1r1o95ripysy1yVuvl-hAEevek4vdqp-Df7slw2hscF4/edit#heading=h.l0ht1p2v2ivs).
Discussion can be found on the [slack channel](https://sfu-big-data.slack.com/messages/G92HNPWJ1/)

### Components
1. Coinmarketcap Scraper
2. Django REST API
3. GitHub Scraper
4. Twitter Scraper
5. Forum Scraper
6. Web Scraper
7. EDA
8. Web Visualization

### Usage
#### Installation
    git clone https://github.com/LinuxIsCool/733Project.git
    cd 733Project
    activate virtual environment
    pip install -r requirements.txt

#### Running the server
    cd CryptViz/
    python manage.py runserver
     
#### CoinMarketCap Scraper
Get list of top 100 coins(ranked by market cap) from coinmarketcap.com

    from CryptViz.Scrapers.Coinmarketcap import coinmarketcap
    cmk = coinmarketcap()
    top_100 = cmk.coin_list

#### Posting to Database
Posting static data for top 100 coins. (Website URL, Git URL, Forum URL)

    for coin in top_100:
    	static_data = cmk.get_static(coin)
	url = "api/" + coin
	requests.post(url, coin_data)

Posting time series data for top 100 coins. One period is one day. (Price, Volume)

    for coin in top_100:
    	daily_data = cmk.get_today(coin)
	url = "api/" + coin + "/cmk/" + datetime.datetime.today().strftime("%D")
	requests.post(url, daily_data)
    
### References
1. [Deep Reinforcement Learning for the Financial Portfolio Management Problem](https://arxiv.org/pdf/1706.10059.pdf) [implementation](https://github.com/ZhengyaoJiang/PGPortfolio) [replication](https://github.com/wassname/rl-portfolio-management)
2. [Evolutionary Dynamics of the Cryptocurrency Market](http://rsos.royalsocietypublishing.org/content/4/11/170623)
3. [coinmarketcap.com](https://coinmarketcap.com/)
4. [Analyzing Cryptocurrency Markets Using Python](https://blog.patricktriest.com/analyzing-cryptocurrencies-python/)
5. [Predicting Cryptocurrency Prices with Deep Learning](https://dashee87.github.io/deep%20learning/python/predicting-cryptocurrency-prices-with-deep-learning/)
