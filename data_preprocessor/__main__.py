from data_preprocessor import clean_dataframe
from data_preprocessor import normalize_dataframe
from data_preprocessor import get_mongo_raw_depression_df


DATASET_PATH = '../resources/data/Depressive data.xlsx'


def main():
    raw_dataset_df = get_mongo_raw_depression_df()
    cleaned_dataset_df = clean_dataframe(raw_dataset_df)    # clean data
    normalized_dataset_df = normalize_dataframe(cleaned_dataset_df)    # normalize data (stopwords removal and lemmas)
    print(normalized_dataset_df.head())
    print(normalized_dataset_df.shape)


if __name__ == "__main__":
    main()
