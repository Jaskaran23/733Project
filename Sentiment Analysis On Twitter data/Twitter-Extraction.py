from pymongo import MongoClient
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime

# The MongoDB connection info. This assumes your database name is TwitterStream, and your collection name is tweets.
connection = MongoClient('localhost', 27017)
db = connection.TwitterDatafinal2
db.finalTweetsfin.ensure_index("id", unique=True, dropDups=True)
collection = db.finalTweetsfin

# Add the keywords you want to track. They can be cashtags, hashtags, or words.
keywords = ['Bitcoin', 'Bitcoin Cash', 'Litecoin', 'Cardano', 'NEO', 'Stellar', 'EOS', 'Dash', 'IOTA', 'Monero', 'NEM', 'Ethereum Classic', 'TRON', 'VeChain', 'Lisk', 'Qtum', 'Bitcoin Gold', 'Bytecoin', 'Binance Coin', 'Dogecoin', 'DigixDAO', 'BitShares', 'KuCoin Shares', 'Cryptonex', 'MonaCoin', 'QASH', 'PIVX', 'Bitcore', 'ReddCoin', 'GXShares', 'ZCoin', 'MaidSafeCoin', 'Vertcoin', 'Particl', 'Enigma', 'Neblio', 'Emercoin', 'TenX', 'Blocknet', 'Request Network', 'SmartCash', 'GameCredits']

# Optional - Only grab tweets of specific language
language = ['en']

# You need to replace these with your own values that you get after creating an app on Twitter's developer portal.
consumer_key = "txHlAA8WIPfg3snXXL5NxdSME"
consumer_secret = "lawdBSNkUo5v0mVh2oalRQ9uinxFAqY7AUIhvDCC31a4Un9zJ3"
access_token = "928088308101431296-IfGbDInIJ2xUy2OCQol6sb8tgUDvcRl"
access_token_secret = "v32CHF8BdcxrTWUfIpjUw0ygbhkwzGnRsGg9iLo4VACCw"

# The below code will get Tweets from the stream and store only the important fields to your database
class StdOutListener(StreamListener):

    def on_data(self, data):

        # Load the Tweet into the variable "t"
        t = json.loads(data)

        # Pull important data from the tweet to store in the database.
        tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
        username = t['user']['screen_name']  # The username of the Tweet author
        followers = t['user']['followers_count']  # The number of followers the Tweet author has
        text = t['text']  # The entire body of the Tweet
        truncated = t['truncated'] # Indicates whether the value of the text parameter was truncated
        statusSource = t['source'] # Utility used to post the Tweet as an HTML-formatted string
        replyToUID = t['in_reply_to_user_id_str'] # The field contains a  string representation of the original Tweet’s author ID,if the tweet is reply
        replyToSN = t['in_reply_to_screen_name'] # The field contains the screen name of the original Tweet’s author,if the tweet is reply
        replyToSID = t['in_reply_to_status_id_str'] # The field contains a  string representation of the original Tweet’s ID,if the tweet is reply
        favorited = t['favorited'] # Indicates whether this Tweet has been liked by the authenticating user
        favoriteCount = t['favorite_count'] # Indicates approximately how many times this Tweet has been liked by Twitter users
        #isRetweeted = t['retweeted_status'] # The users can amplify the broadcast of Tweets authored by other users by retweeting
        retweeted = t['retweeted'] # Indicates whether this Tweet has been Retweeted by the authenticating user
        retweetCount = t['retweet_count'] # Number of times this Tweet has been retweeted
        hashtags = t['entities']['hashtags']  # Any hashtags used in the Tweet
        dt = t['created_at']  # The timestamp of when the Tweet was created
        language = t['lang']  # The language of the Tweet

        # Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
        created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'truncated':truncated, 
                 'statusSource':statusSource, 'replyToUID':replyToUID, 'replyToSN':replyToSN, 'replyToSID':replyToSID, 
                 'favorited':favorited, 'favoriteCount':favoriteCount, 'retweeted':retweeted, 
                 'retweetCount':retweetCount,'hashtags':hashtags, 'language':language, 'created':created}

        # Save the refined Tweet data to MongoDB
        collection.save(tweet)

        # Optional - Print the username and text of each Tweet to your console in realtime as they are pulled from the stream
        print(username + ':' + ' ' + text)
        return True

    # Prints the reason for an error to your console
    def on_error(self, status):
        print(status)

# Some Tweepy code that can be left alone. It pulls from variables at the top of the script
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
stream.filter(track=keywords, languages=language)
