from data_converter import convert_xlsx_to_dataframe
from data_cleaner import clean_dataframe


DATASET_PATH = '../resources/data/Depressive data.xlsx'


def main():
    raw_dataset_df = convert_xlsx_to_dataframe(DATASET_PATH)
    cleaned_dataset_df = clean_dataframe(raw_dataset_df)
    print(cleaned_dataset_df.head())
    print(cleaned_dataset_df.shape)


if __name__ == "__main__":
    main()
