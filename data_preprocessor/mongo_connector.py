import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import urllib.parse

CONNECTION_STRING = "mongodb://user:" + urllib.parse.quote("pass") + "@host:port/database?retryWrites=true&w=majority"


def get_mongo_raw_depression_df(do_remove_id=True):
    client = MongoClient(CONNECTION_STRING)
    db = client['depression']
    raw_data_collection = db['raw_depression_data']
    raw_data_cursor = raw_data_collection.find()

    dataframe = pd.DataFrame(list(raw_data_cursor))
    if do_remove_id:
        del dataframe['_id']

    return dataframe


def upload_mongo_preprocessed_df(dataframe):
    client = MongoClient(CONNECTION_STRING)
    db = client['depression']
    collection_name = f'preprocessed_depression_data_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
    preprocessed_data_collection = db[collection_name]
    inserted_json = dataframe.to_dict('records')
    preprocessed_data_collection.insert_many(inserted_json)
