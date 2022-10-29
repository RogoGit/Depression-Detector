import pandas

from data_cleaner import clean_dataframe
from data_normalizer import normalize_dataframe
from mongo_connector import get_mongo_raw_depression_df, upload_mongo_preprocessed_df
from data_augmentator import augmentate_dataframe


DATASET_PATH = '../resources/data/Depressive data.xlsx'


def main():
    # pandas.set_option('display.max_rows', None)   - show full df, use for debug purpose
    raw_dataset_df = get_mongo_raw_depression_df()
    cleaned_dataset_df = clean_dataframe(raw_dataset_df)    # clean data
    augmented_dataset_df = augmentate_dataframe(cleaned_dataset_df)     # create new entries with text noising
    normalized_dataset_df = normalize_dataframe(augmented_dataset_df)    # normalize data (stopwords removal and lemmas)
    print(normalized_dataset_df.head())
    print(normalized_dataset_df.shape)
    upload_mongo_preprocessed_df(normalized_dataset_df)


if __name__ == "__main__":
    main()
