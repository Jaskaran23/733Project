# Big Data II Final Project: CryptViz
Can we visualize the cryptocurrency ecosystem?

### About
Information can be found here in the [project proposal](https://docs.google.com/document/d/1r1o95ripysy1yVuvl-hAEevek4vdqp-Df7slw2hscF4/edit#heading=h.l0ht1p2v2ivs).
Discussion can be found on the [slack channel](https://sfu-big-data.slack.com/messages/G92HNPWJ1/)

### Components
1. Coinmarketcap Scraper
2. GitHub Scraper
3. [Exploratory Data Analysis with Pandas](https://github.com/LinuxIsCool/733Project/blob/master/CryptViz/CoinMarketcapEDA.ipynb)
4. [Price Prediction with CNN](https://github.com/LinuxIsCool/733Project/blob/master/CryptViz/CNNPrediction.ipynb)
5. [Price Prediction with LSTM]()
6. Twitter Streaming
7. [Twitter Integration and Analysis]()

### Usage
#### Installation
Download

	git clone https://github.com/LinuxIsCool/733Project.git
	cd 733Project

Create or Activate virtual environment

	# With Conda
	conda new 733Project
	conda activate 733Project

	# Or with virtualenv
	virtualenv venv
	source venv/bin/activate

Install Requirements

	pip install -r requirements.txt

Install kernal to use in jupyter notebooks

	ipython kernel install --user --name=733Project


#### Launching the Notebooks
	jupyter-notebook CoinMarketcap.ipynb
     
#### CoinMarketCap Scraper
Get list of top 100 coins(ranked by market cap) from coinmarketcap.com

	from Scrapers.Coinmarketcap import coinmarketcap
	cmk = coinmarketcap.CoinMarketcap()
	coins = cmk.coin_names()

    
### References
1. [Deep Reinforcement Learning for the Financial Portfolio Management Problem](https://arxiv.org/pdf/1706.10059.pdf) [implementation](https://github.com/ZhengyaoJiang/PGPortfolio) [replication](https://github.com/wassname/rl-portfolio-management)
2. [Evolutionary Dynamics of the Cryptocurrency Market](http://rsos.royalsocietypublishing.org/content/4/11/170623)
3. [coinmarketcap.com](https://coinmarketcap.com/)
4. [Analyzing Cryptocurrency Markets Using Python](https://blog.patricktriest.com/analyzing-cryptocurrencies-python/)
5. [Predicting Cryptocurrency Prices with Deep Learning](https://dashee87.github.io/deep%20learning/python/predicting-cryptocurrency-prices-with-deep-learning/)
