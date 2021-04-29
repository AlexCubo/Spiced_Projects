from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import logging
import os
from dotenv import load_dotenv

'''
load_dotenv()
logging.basicConfig(level=logging.INFO)

try:
    client = MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS=1000)
     # force connection on a simple request
    client.server_info()  
    logging.info('connected to mongodb')         
except ServerSelectionTimeoutError as e:
    logging.error("could not connect to mongodb")      

try:
    engine = create_engine(os.getenv('POSTGRESDB_URI'))
    engine.execute('select 1 as is_alive;')
    logging.info('connected to postgresdb')
except OperationalError as e:
   logging.error("could not connect to postgresdb")
'''