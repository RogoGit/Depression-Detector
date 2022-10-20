import pandas as pd


def convert_xlsx_to_dataframe(file_path):
    depression_dataset_df = pd.read_excel(file_path)
    return depression_dataset_df
