import pandas as pd
import time


def convert_xlsx_to_dataframe(file_path):
    print("Started conversion")
    start_time = time.time()
    depression_dataset_df = pd.read_excel(file_path)
    print("Finished conversion, took: %s seconds" % (time.time() - start_time))
    return depression_dataset_df
