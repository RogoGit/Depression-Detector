from lstm_model import DepressionClassifierModel, ModelTrainer, fit
import torch.nn as nn
import torch.optim as optim


def init_trainer(model):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters())
    trainer = ModelTrainer(model, criterion, optimizer)
    return trainer


def start_training(trainer, train_iter, val_iter):
    fit(trainer, train_iter, epochs_count=20, val_iter=val_iter)
