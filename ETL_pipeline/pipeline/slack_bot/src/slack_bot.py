# pip install pyjokes
import pyjokes
import requests
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import logging
import time
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import random

load_dotenv()

try:
    engine = create_engine(os.getenv('POSTGRESDB_URI'))
    engine.execute('select 1 as is_alive;')
    logging.info('connected to postgresdb')
except OperationalError as e:
   logging.error("could not connect to postgresdb")

query_str = "SELECT screen_name, text, compound FROM tweets"
with engine.connect() as conn:
   result = conn.execute(query_str)
print(result.rowcount)

df =pd.DataFrame(result)
twitts = {'author':df[0], 'twitt':df[1], 'sentiment':df[2]}


#starting loop for automated twitt diploy
numTimes = 10
n = 0
while n < numTimes:
    n += 1
    #pick a random twitt between teh ones we have
    ranNum = random.randint(1,len(twitts['twitt']))
    #print(ranNum)

    randTwitt = 'Author: ' + twitts['author'][ranNum] + '\n' +\
                'Twitt: ' + twitts['twitt'][ranNum] +  '\n'\
                'Feeling: ' + str(twitts['sentiment'][ranNum])

    #print(randTwitt)

    webhook_url = os.getenv('SLACK_WEBHOOK_URL')

    print('SLACK_BOT ENDED!')
    joke = pyjokes.get_joke()

    data = {'text': randTwitt}
    requests.post(url=webhook_url, json = data)
    #print(f'Text {n} sent to Slack!!')

    #wait 15 minutes
    time.sleep(900)
