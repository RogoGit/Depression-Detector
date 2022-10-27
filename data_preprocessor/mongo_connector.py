import pandas as pd
from pymongo import MongoClient

CONNECTION_STRING = "0.05(6)"


def get_mongo_raw_depression_df(do_remove_id=True):
    client = MongoClient(CONNECTION_STRING)
    db = client['depression']
    raw_data_collection = db['raw_depression_data']
    raw_data_cursor = raw_data_collection.find()

    dataframe = pd.DataFrame(list(raw_data_cursor))
    if do_remove_id:
        del dataframe['_id']

    return dataframe

