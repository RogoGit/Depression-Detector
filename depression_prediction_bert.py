# -*- coding: utf-8 -*-
"""DepressionPredictionBERT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19RtWN8EE8GcHMCvF0WsCWh4v_oPTO7tf

## БИБЛЫ
"""

from google.colab import drive
drive.mount('/content/drive')

pip install mlflow

pip install evaluate

pip install datasets

pip install transformers

import torch
import numpy as np
np.random.seed(313)

torch.torch_version.internal_version

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import re

"""## Загрузка данных"""

CONNECTION_STRING = ""

def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def get_latest_preprocessed_depression_df(do_remove_id=True, do_remove_age=True):
    client = MongoClient(CONNECTION_STRING)
    print(client.list_database_names())
    db = client['depression']
    print(db.list_collection_names())
    preprocessed_collections = [coll for coll in db.list_collection_names() if 'preprocessed_depression_data' in coll]
    preprocessed_collections.sort(key=natural_keys)
    latest_collection_name = 'preprocessed_depression_data_10_12_2022_17_01_54'
    latest_preprocessed_data_collection = db[latest_collection_name]
    preprocessed_data_cursor = latest_preprocessed_data_collection.find()
    dataframe = pd.DataFrame(list(preprocessed_data_cursor))
    if do_remove_id:
        del dataframe['_id']
    if do_remove_age:
        del dataframe['age']
    print(dataframe)
    return dataframe

depression_df = get_latest_preprocessed_depression_df()

"""##Разделение на train, test"""

from sklearn.model_selection import train_test_split

train_df, test_df = train_test_split(depression_df, test_size=0.20, random_state=313, stratify=depression_df['label'])

print(train_df)
print(test_df)

"""## Преобразование к нужному для обработки виду"""

from datasets import Dataset

ds_train = Dataset.from_pandas(train_df)
ds_test = Dataset.from_pandas(test_df)

"""## Токенизация"""

from transformers import AutoTokenizer, DataCollatorWithPadding

# DeepPavlov/distilrubert-tiny-cased-conversational-v1
# DeepPavlov/distilrubert-tiny-cased-conversational
tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

def tokenize(dataset):
    return tokenizer(dataset["text"], truncation=True, max_length=512, padding='max_length')

tokenized_ds_train = ds_train.map(tokenize, batched=True)
tokenized_ds_test = ds_test.map(tokenize, batched=True)
print(tokenized_ds_train)

"""## Оценщик"""

import evaluate
import numpy as np
from transformers import EvalPrediction

accuracy = evaluate.load("accuracy")
f1 = evaluate.load("f1")
pr = evaluate.load("precision")
r = evaluate.load("recall")

def compute_metrics(p: EvalPrediction):
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    preds = np.argmax(preds, axis=1)
    result = {}
    result["accuracy"] = accuracy.compute(predictions=preds, references=p.label_ids)["accuracy"]
    result["f1"] = f1.compute(predictions=preds, references=p.label_ids)["f1"]
    result["precision"] = pr.compute(predictions=preds, references=p.label_ids)["precision"]
    result["recall"] = r.compute(predictions=preds, references=p.label_ids)["recall"]
    return result

"""## Классификатор депрессии"""

id2label = {"0": "NON-DEPRESSIVE", "1": "DEPRESSIVE"}
label2id = {"NON-DEPRESSIVE": "0", "DEPRESSIVE": "1"}

import mlflow
import os

# https://huggingface.co/docs/transformers/v4.20.1/en/main_classes/callback#transformers.integrations.MLflowCallback

os.environ["MLFLOW_EXPERIMENT_NAME"] = "Depression Classifier"
os.environ["MLFLOW_FLATTEN_PARAMS"] = "1"
os.environ["MLFLOW_TRACKING_URI"]=""
os.environ["HF_MLFLOW_LOG_ARTIFACTS"]="1"

from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

mlflow.start_run()

model = AutoModelForSequenceClassification.from_pretrained(
    "DeepPavlov/rubert-base-cased", num_labels=2, id2label=id2label, label2id=label2id
)

training_args = TrainingArguments(
    output_dir="/content/drive/MyDrive/Colab Notebooks/rubert-base-b8-ep1",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=1,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    label_names = ["labels"],
    logging_steps=1,
    metric_for_best_model='accuracy',
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds_train,
    eval_dataset=tokenized_ds_test,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()

mlflow.end_run()

"""## Произвольные запросы"""

from transformers import pipeline

classifier = pipeline("text-classification", model="/content/drive/MyDrive/Colab Notebooks/rubert-base-b8-ep1/checkpoint-6256")  # path to model

print(classifier("Как же хочется сдохнуть"))
print(classifier("Я обожаю свою жизнь"))
print(classifier("Меня зовут Никита мне 23 года"))
print(classifier("Нет не женат, на рыбалочку да с гитарой, было бы не плохо с тебя удочки, с меня гитара"))
print(classifier("на рыбалочку да с гитарой, было бы не плохо с тебя удочки, с меня гитара"))
print(classifier("Случайное сообщение пишу что в голову взбредет автобус помидоры мазик"))
print(classifier("Высота снежного покрова в Москве за сутки выросла на 14 см"))
print(classifier("Заходите люди поиграть в war thunder тут очень красиво"))
print(classifier("Приветик))))))"))
print(classifier("Благодаря введенному накануне потолку цен на российскую нефть Китай сможет покупать больше топлива из России с большой скидкой, в то время как российская сторона будет по-прежнему получать от продажи нефти высокую прибыль."))
print(classifier("Как у вас делишки? У меня вот все хорошо, женился на любимой девушке, нашел работу за 30000к бачей с релокейтом в ЧГ!"))

print(classifier("Суицид хочу умереть"))
print(classifier("Картошка хочу жить"))
print(classifier("девушка бросила"))
print(classifier("приятно прогуляться по улице в хороший денек"))
