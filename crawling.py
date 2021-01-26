import json
import snscrape.modules.twitter as snstwitter
import tweepy
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db_client = client['cosrx_db']
collection = db_client['crawling_1']

CONSUMER_KEY = "ER6dm8K9Y2gGm4w3vHhJIxy8o"
CONSUMER_SECRET = "InYaTVJjmIsG3PMp5nKOU6bMUXIyT7kHoJXtVXxsLYh9w1YOS5"
ACCESS_TOKEN = "1330751702136365056-doRSWEBA00wZzOL03hXVMI5qTP2cDe"
ACCESS_TOKEN_SECRET = "ZxCgwpV05w4cjRbUlhPyajUvvSwL5E9bZqVUQxjRTAE1c"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
last_id_saver = 'last_id.txt'
if (not api):
    sys.exit('Autentikasi gagal')
else:
    print("Berasil")

search_words = ['cosrx', 'skincare cosrx']
tweets = tweepy.Cursor(api.search, q=search_words, lang="in",
                       since='2019-01-01', tweet_mode='extended').items()
while True:
    # as long as I still have a tweet to grab
    try:
        data = tweets.next()
    except StopIteration:
        break
    # convert from Python dict-like structure to JSON format
    jsoned_data = json.dumps(data._json)
    tweet = json.loads(jsoned_data)
    # insert the information in the database
    collection.insert_one(tweet)
    count += 1
    print('tweet tersimpan : ',  count)
