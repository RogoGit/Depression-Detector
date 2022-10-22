import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem

nltk.download("stopwords")
mystem = Mystem()
russian_stopwords = stopwords.words("russian")


def normalize_dataframe(depression_data_df):
    for idx, data_row in depression_data_df.iterrows():
        tokens = mystem.lemmatize(str(data_row['text']).lower())
        tokens = [token for token in tokens if token not in russian_stopwords and token != " "]
        normalized_text = " ".join(tokens)
        depression_data_df.at[idx, 'text'] = normalized_text
    return depression_data_df
