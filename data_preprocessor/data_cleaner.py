import pandas as pd
import re
from spell_checker import fix_typos


def clean_dataframe(depression_data_df):
    for idx, data_row in depression_data_df.iterrows():
        post_text = str(data_row['text']).lower()

        # -- remove 'bad' records

        # remove records with unrealistic age
        if not pd.isnull(data_row['age']) and int(data_row['age']) > 100:
            depression_data_df.drop(idx, inplace=True)
            continue

        # remove records with unreachable twitter pics
        if 'pic.twitter.com' in post_text:
            depression_data_df.drop(idx, inplace=True)
            continue

        # remove records which contain only 'добрый вечер' and similar
        words_to_search = ['здравствуйте', 'привет', 'добрый', 'доброе', 'лет']
        if len(post_text.split()) <= 3 and any(word in post_text for word in words_to_search):
            depression_data_df.drop(idx, inplace=True)
            continue

        # -- clean 'good' records

        # remove links
        post_text = ' '.join(re.sub("http\S+", " ", post_text).split())
        # remove hashtags, @mentions, emojis
        post_text = ' '.join(re.sub("(@[А-Яа-яA-Za-z0-9]+)|(#[А-Яа-яA-Za-z0-9]+)|(<Emoji:.*>)", " ", post_text).split())
        # remove punctuation and fix word-dot-word without space
        post_text = ' '.join(re.sub("([^0-9A-Za-zА-Яа-я \t])", " ", post_text).split())
        # try to fix typos
        # post_text = fix_typos(post_text)
        depression_data_df.at[idx, 'text'] = post_text

    return depression_data_df
