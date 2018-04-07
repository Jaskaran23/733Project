import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from ggplot import *
from wordcloud import WordCloud
from wordcloud import STOPWORDS

%matplotlib inline
import matplotlib.pyplot as plt

tweets = pd.read_csv('C:/Users/Vimo/Documents/Big Data -733/733Project/TwitterDatafinal2.finalTweetsfin.csv', parse_dates=['created'], header=0, encoding="ISO-8859-1")

plt.rcParams['figure.figsize'] = (6.0, 6.0)

sentiment_id = SentimentIntensityAnalyzer()

tweets['polarity']=tweets.text.apply(lambda x:sentiment_id.polarity_scores(x)['compound'])
tweets['sentiment_negative']=tweets.text.apply(lambda x:sentiment_id.polarity_scores(x)['neg'])
tweets['sentiment_neutral']=tweets.text.apply(lambda x:sentiment_id.polarity_scores(x)['neu'])
tweets['sentiment_positive']=tweets.text.apply(lambda x:sentiment_id.polarity_scores(x)['pos'])
tweets['sentiment_type']=''
tweets.loc[tweets.polarity<0,'sentiment_type']='NEGATIVE'
tweets.loc[tweets.polarity==0,'sentiment_type']='NEUTRAL'
tweets.loc[tweets.polarity>0,'sentiment_type']='POSITIVE'
print("Summary of Tweets:")
print(tweets.sentiment_type.value_counts(sort=False))

#display(tweets.polarity)

#display(tweets.head(15))  #for testing 
#colors = ['green','blue','red']
#tweets.sentiment_type.value_counts(sort=False).plot(kind='bar', title="Sentiment Analysis", color=colors)
#plt.xlabel('Sentiment Score', fontweight='bold')
#plt.ylabel('Tweets Count', fontweight='bold')

tweets['hour'] = pd.DatetimeIndex(tweets['created']).hour
tweets['date'] = pd.DatetimeIndex(tweets['created']).date
tweets['minute'] = pd.DatetimeIndex(tweets['created']).minute
df=(tweets.groupby('hour',as_index=False).polarity.mean())
print(ggplot(aes(x='hour',y='polarity'),data=df)+geom_line()+ ggtitle("Polarity per hour"))

print(ggplot(tweets, aes(x='sentiment_type', y='sentiment_type.value_counts(sort=False)')) +\
    geom_bar() +\
    xlab("Sentiment Score") + ylab("Tweets Count") + ggtitle("Sentiment Analysis")) #+\
    #scale_fill_manual(values = color("#DD0426","#246EB9","#04B430"))
tweets['count'] = 1
tweets_filtered = tweets[['hour', 'date', 'count', 'retweetCount']]
tweets_filtered.head(2)

tweets_hourly = tweets_filtered.groupby(["hour"]).sum().reset_index()
tweets_hourly.head(2)

f, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

ax1.title.set_text("Number of tweets per hour")
tweets_hourly["count"].plot.bar(ax=ax1, color='#999966')
tweets_hourly["count"].plot(ax=ax1)

ax2.title.set_text("Number of re-tweets per hour")
tweets_hourly["retweetCount"].plot.bar(ax=ax2)
tweets_hourly["retweetCount"].plot(ax=ax2, color='#999966')

pivot_df = tweets_filtered.pivot_table(tweets_filtered, index=["date", "hour"], aggfunc=np.sum)
print(pivot_df)
dates = pivot_df.index.get_level_values(0).unique()

f, ax = plt.subplots(2, 1, figsize=(8, 10))
plt.setp(ax, xticks=list(range(0,24)))

ax[0].title.set_text("Number of tweets per hour")
ax[1].title.set_text("Number of re-tweets per hour")

for date in dates:
    split = pivot_df.xs(date)
    
    split["count"].plot(ax=ax[0], legend=True, label='' + str(date))
    split["retweetCount"].plot(ax=ax[1], legend=True, label='' + str(date))       


def wordcloud_by_province(tweets):
    stopwords = set(STOPWORDS)
    stopwords.add("https")
    stopwords.add("00A0")
    stopwords.add("00BD")
    stopwords.add("00B8")
    stopwords.add("ed")
    wordcloud = WordCloud(background_color="black",width=480,height=480, margin=0,stopwords=stopwords,max_font_size=70, random_state =2000).generate(" ".join([i for i in tweets['text'].str.upper()]))
    plt.figure()
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.margins(x=0, y=0)
    plt.axis("off")
    plt.title("CRYPTOCURRENCY")
    
wordcloud_by_province(tweets)
