from pytrends.request import TrendReq

pytrends = TrendReq()

suggestions_dict = pytrends.suggestions(keyword='CryptoCurrency')
print(suggestions_dict)

kw_list = ["Blockchain","Cryptocurrency"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='News')
interest_over_time_df = pytrends.interest_over_time()
print(interest_over_time_df)

interest_by_region = pytrends.interest_by_region(resolution='COUNTRY')
print(interest_by_region[interest_by_region['Cryptocurrency']>0].sort_values('Cryptocurrency', ascending=False))