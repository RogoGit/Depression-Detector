import pandas as pd


def clean_dataframe(depression_data_df):
    for i, data_row in depression_data_df.iterrows():

        # remove records with unrealistic age
        if not pd.isnull(data_row['age']) and int(data_row['age']) > 100:
            depression_data_df.drop(i, inplace=True)
            continue

    return depression_data_df
