import random
import pandas as pd
from alive_progress import alive_bar

word_swaps_per_document = 10
word_drop_per_document = 4
typos_and_character_swaps_per_document = 10
number_of_generated_messages_for_one = 3


def random_swap(text):
    token_list = text.split()
    for i in range(word_swaps_per_document):
        tokens_to_swap = random.sample(token_list, 2)
        token_list[token_list.index(tokens_to_swap[0])], token_list[token_list.index(tokens_to_swap[1])] =\
            token_list[token_list.index(tokens_to_swap[1])], token_list[token_list.index(tokens_to_swap[0])]
    return ' '.join(token_list)


def random_drop(text):
    token_list = text.split()
    if len(token_list) > 10:
        tokens_to_delete = random.sample(token_list, word_drop_per_document)
        return ' '.join([item for item in token_list if item not in tokens_to_delete])
    else:
        return text


def random_character_swap(text):
    token_list = text.split()
    tokens_to_swap_characters = [item for item in token_list if len(item) >= 2]
    if len(tokens_to_swap_characters) >= typos_and_character_swaps_per_document:
        chosen_tokens_to_swap_characters = random.sample(tokens_to_swap_characters, typos_and_character_swaps_per_document)
        for i, token in enumerate(token_list):
            if token in chosen_tokens_to_swap_characters:
                character_index = random.randint(0, len(token)-2)
                chosen_token_list = list(token)
                chosen_token_list[character_index], chosen_token_list[character_index + 1] =\
                    chosen_token_list[character_index + 1], chosen_token_list[character_index]
                token_list[i] = str(''.join(chosen_token_list))
        return ' '.join(token_list)
    else:
        return text


def augmentate_dataframe(depression_data_df):
    print("Started augmentation")
    generated_entries = []
    with alive_bar(depression_data_df.shape[0], dual_line=True, title='Augmentation') as bar:
        for idx, data_row in depression_data_df.iterrows():
            post_text = data_row['text']
            for i in range(number_of_generated_messages_for_one):
                swapped = random_swap(post_text)
                deleted = random_drop(swapped)
                augmented = random_character_swap(deleted)
                generated_entries.append({'text': augmented, 'label': data_row['label'], 'age': data_row['age']})
            bar()
    depression_data_augmented_df = pd.DataFrame(generated_entries)
    final_df = pd.concat([depression_data_df, depression_data_augmented_df], ignore_index=True)
    print("Finish augmentation")
    return final_df
