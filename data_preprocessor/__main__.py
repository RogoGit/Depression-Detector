from data_converter import convert_xlsx_to_dataframe
from data_cleaner import clean_dataframe
from data_normalizer import normalize_dataframe


DATASET_PATH = '../resources/data/Depressive data.xlsx'


def main():
    raw_dataset_df = convert_xlsx_to_dataframe(DATASET_PATH)
    cleaned_dataset_df = clean_dataframe(raw_dataset_df)    # clean data
    normalized_dataset_df = normalize_dataframe(cleaned_dataset_df)    # normalize data (stopwords removal and lemmas)
    print(normalized_dataset_df.head())
    print(normalized_dataset_df.shape)


if __name__ == "__main__":
    main()
