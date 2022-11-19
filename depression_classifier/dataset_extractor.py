import re
import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from torchtext.data import Field, LabelField, Example, Dataset, BucketIterator

CONNECTION_STRING = ""


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def get_latest_preprocessed_depression_df(do_remove_id=True, do_remove_age=True):
    client = MongoClient(CONNECTION_STRING)
    db = client['depression']
    preprocessed_collections = [coll for coll in db.list_collection_names() if 'preprocessed_depression_data' in coll]
    preprocessed_collections.sort(key=natural_keys)
    latest_collection_name = preprocessed_collections[-1]
    latest_preprocessed_data_collection = db[latest_collection_name]
    preprocessed_data_cursor = latest_preprocessed_data_collection.find()
    dataframe = pd.DataFrame(list(preprocessed_data_cursor))
    if do_remove_id:
        del dataframe['_id']
    if do_remove_age:
        del dataframe['age']
    return dataframe


def split_to_samples(depression_df):
    train_df, test_df = train_test_split(depression_df, test_size=0.20, random_state=313, stratify=depression_df['label'])
    train_df, val_df = train_test_split(train_df, test_size=0.10, random_state=313, stratify=train_df['label'])
    return train_df, val_df, test_df


def df_to_list(df):
    data_list = []
    for idx, data_row in df.iterrows():
        data_list.append(([word.strip() for word in data_row['text'].strip().split()], data_row['label']))
    return data_list


def create_dataset_iters():
    depression_df = get_latest_preprocessed_depression_df()
    train_df, val_df, test_df = split_to_samples(depression_df)

    tokens_field = Field()
    label_field = LabelField()

    fields = [('tokens', tokens_field), ('label', label_field)]

    train_dataset = Dataset([Example.fromlist(example, fields) for example in df_to_list(train_df)], fields)
    val_dataset = Dataset([Example.fromlist(example, fields) for example in df_to_list(val_df)], fields)
    test_dataset = Dataset([Example.fromlist(example, fields) for example in df_to_list(test_df)], fields)

    tokens_field.build_vocab(train_dataset)
    label_field.build_vocab(train_dataset)

    # print('Vocab size =', len(tokens_field.vocab))

    train_iter, val_iter, test_iter = BucketIterator.splits(
        datasets=(train_dataset, val_dataset, test_dataset), batch_sizes=(32, 128, 128),
        shuffle=True, sort=False
    )

    return tokens_field, train_iter, val_iter, test_iter
