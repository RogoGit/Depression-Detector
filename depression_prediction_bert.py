import torch
import numpy as np
np.random.seed(313)

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
    latest_collection_name = 'preprocessed_depression_data_12_12_2022_22_59_04'
    latest_preprocessed_data_collection = db[latest_collection_name]
    preprocessed_data_cursor = latest_preprocessed_data_collection.find()
    dataframe = pd.DataFrame(list(preprocessed_data_cursor))
    if do_remove_id:
        del dataframe['_id']
    if do_remove_age:
        del dataframe['age']
    dataframe['label'] = dataframe['label'].astype(int)
    print(dataframe)
    return dataframe

depression_df = get_latest_preprocessed_depression_df()

"""##Разделение на train, test"""

from sklearn.model_selection import train_test_split

train_df, test_df = train_test_split(depression_df, test_size=0.10, random_state=313, stratify=depression_df['label'])

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
# DeepPavlov/distilrubert-base-cased-conversational
tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
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

id2label = {0: "NON-DEPRESSIVE", 1: "DEPRESSIVE"}
label2id = {"NON-DEPRESSIVE": 0, "DEPRESSIVE": 1}

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
    "cointegrated/rubert-tiny2", num_labels=2, id2label=id2label, label2id=label2id
)

training_args = TrainingArguments(
    output_dir="/content/drive/MyDrive/Colab Notebooks/merged-dataset-rubert-tiny2-b8-ep1",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=1,
    weight_decay=0.001,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    label_names=["labels"],
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
