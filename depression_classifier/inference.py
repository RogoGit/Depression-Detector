from autocorrect import Speller
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
import re
import torch

nltk.download("stopwords")
mystem = Mystem()
russian_stopwords = stopwords.words("russian")

speller = Speller('ru')


def preprocess_text(text):
    # remove links
    text = ' '.join(re.sub("http\S+", " ", text).split())
    # remove hashtags, @mentions, emojis
    text = ' '.join(re.sub("(@[А-Яа-яA-Za-z0-9]+)|(#[А-Яа-яA-Za-z0-9]+)|(<Emoji:.*>)", " ", text).split())
    # remove punctuation and fix word-dot-word without space
    text = ' '.join(re.sub("([^0-9A-Za-zА-Яа-я \t])", " ", text).split())
    # try to fix typos

    text = speller(text)
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords and token != " "]
    text = " ".join(tokens)
    return text


def infer(text, model, tokens_field):
    print('---------')
    print('Sentence: ' + text)
    print('---------\n')
    tokens = torch.IntTensor([[tokens_field.vocab.stoi[i] for i in text.split()]])
    predicted_label = model(tokens).argmax(dim=1)
    print(predicted_label)
