import config
from tweepy import OAuthHandler, Cursor, API
from tweepy.streaming import StreamListener
import logging
import pymongo

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S:',
    filename = '/log/twitter_collector.log',
    filemode = 'w')

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 2 required authentication tokens:

       1. API_KEY
       2. API_SECRET
     
    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(config.API_KEY, config.API_SECRET)
    return auth

users = ['POTUS', 'BBCBreaking', 'Blklivesmatter', 'Friday4Future', 'amnesty',
            'NBA', 'F1', 'Cristiano', 'PHarry_Meghan', 'BonoVox_', 'imrobertdeniro',
             'GretaThunberg', 'lunarossa', 'americascup', 'TheGhibliFamily',
             'berlinale', 'cannes', 'GuinnessIreland', 'ChampionsLeague', 'Disney',
             'Ferrero_EU', 'Ferrari', 'NASA', 'TheAmandaGorman', 'LewisHamilton',
             'WWF', 'StephenKing', 'RealRonHoward']
tweets = []

if __name__ == '__main__':
    auth = authenticate()
    api = API(auth)

for user in users:
    cursor = Cursor(
    api.user_timeline,
    id = user,
    tweet_mode = 'extended')

    for status in cursor.items(20):
        tweet = {}
        #print(status.full_text, status.created_at)
        tweet['name'] = status.user.screen_name
        tweet['text'] = status.full_text
        tweet['created_at'] = status.created_at
        #print(tweet)
        tweets.append(tweet)

client = pymongo.MongoClient("mongodb://my_mongodb:27017/")
#name you database
# this initialize only the database but is not visible in mongo
# --> we have to put data inside
db = client.mongoTweets 

#db.tweet_coll1.insert_one(tweets[0])

db.tweet_coll1.drop() 

db.tweet_coll1.insert_many(tweets[:])


logging.info('Twitter collected in MongoDB! Twitter_collector.py ends!!\n\n')
