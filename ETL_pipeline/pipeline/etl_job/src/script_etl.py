# import needed librabries
import pymongo
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import logging
import time
import os
from sqlalchemy.exc import OperationalError
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()
logging.basicConfig(level=logging.INFO)

time.sleep(50)

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S:',
    filename = '/log/etl.log',
    filemode = 'w')

logging.info('ETL JOB STARTED')

#define connections fo mongodb and postgres within the docker container pipeline
#####client = pymongo.MongoClient("mongodb://my_mongodb:27017")

try:
    client = pymongo.MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS=3000)
     # force connection on a simple request
    client.server_info()  
    logging.info('connected to mongodb')         
except ServerSelectionTimeoutError as e:
    logging.error("could not connect to mongodb")


#print(os.getenv("MONGODB_URI"))
#logging.debug('Connected to Mongo Client!')

#connecting to postgres
####engine = create_engine("postgresql://postgres:my_p0stgres@my_postgres:5432/psqlTweets")
try:
    engine = create_engine(os.getenv('POSTGRESDB_URI'))
    engine.execute('select 1 as is_alive;')
    logging.info('connected to postgresdb')
except OperationalError as e:
   logging.error("could not connect to postgresdb")


# EXTRACT data from mongodb 
# client.mongoTweets is the same as db (in twitter_collector)
extraction = client.mongoTweets.tweet_coll1.find()

# TRANFORM data to wanted structure
tf_data = {'screen_name':[], 'text':[], 'date':[], 'sentiment':[]}
for doc in extraction:
    tf_data['screen_name'].append(doc['name'].upper())
    tf_data['text'].append(doc['text'])
    tf_data['date'].append(doc['created_at'])

# initialize Sentiment Analizer
s_analyzer = SentimentIntensityAnalyzer(
                                        lexicon_file='/utils/vader_lexicon.txt',
                                        emoji_lexicon='/utils/emoji_utf8_lexicon.txt')

# Determine sentiment of tweet
for tweet in tf_data['text']:
    #print(tweet)
    sentiment = s_analyzer.polarity_scores(tweet)
    tf_data['sentiment'].append(sentiment)

# Dividing scores
expanded_data = {'screen_name':[], 'text':[], 'date':[], 
                'neg':[], 'neu':[], 'pos': [], 'compound':[]}

for t in range(len(tf_data['text'])):
    expanded_data['screen_name'].append(tf_data['screen_name'][t])
    expanded_data['text'].append(tf_data['text'][t])
    expanded_data['date'].append(tf_data['date'][t])
    expanded_data['neg'].append(tf_data['sentiment'][t]['neg'])
    #print('Negativ', tf_data['sentiment'][t]['neg'])
    expanded_data['neu'].append(tf_data['sentiment'][t]['neu'])
    #print('Neutral', tf_data['sentiment'][t]['neu'])
    expanded_data['pos'].append(tf_data['sentiment'][t]['pos'])
    #print('Positive', tf_data['sentiment'][t]['pos'])
    expanded_data['compound'].append(tf_data['sentiment'][t]['compound'])
    #print('Compound', tf_data['sentiment'][t]['compound'])

df = pd.DataFrame(tf_data)
exp_df = pd.DataFrame(expanded_data)
#print(exp_df[['neg', 'neu', 'pos', 'compound']])

#print number of tweets saved
for k,v in tf_data.items():
    #logging.info('Field', k)
    #logging.info('Length is', len(v))
    print('Field', k, 'and length', len(v))


df.to_csv('/log/tweet_sent.csv', index = False)
exp_df.to_csv('/log/tweet_sent_exp.csv', index = False)

if len(exp_df) == 0:
#    print('No data in the data frame after transformation!')
    logging.warning('no data in the data frame after transformation!')

# LOAD data into database for use later
exp_df.to_sql('tweets', engine, if_exists='replace', index=False)

logging.info('ETL JOB ENDED')

