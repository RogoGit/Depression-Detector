import torch
import torch.nn as nn
from tqdm import tqdm
tqdm.get_lock().locks = []


class DepressionClassifierModel(nn.Module):
    def __init__(self, vocab_size, emb_dim=64, lstm_hidden_dim=128, num_layers=1, dropout_p=0.2):
        super().__init__()

        self.embeddings_layer = nn.Embedding(vocab_size, emb_dim)
        self.dropout = nn.Dropout(dropout_p)
        self.lstm_layer = nn.LSTM(input_size=emb_dim, hidden_size=lstm_hidden_dim, bidirectional=True,
                                  num_layers=num_layers, batch_first=True)
        self.out_layer = nn.Linear(lstm_hidden_dim * 2, 2)

    def forward(self, inputs):
        projections = self.embeddings_layer(inputs)
        _, (final_hidden_state, _) = self.lstm_layer(projections)
        hidden = self.dropout(torch.cat([final_hidden_state[0], final_hidden_state[1]], dim=1))
        output = self.out_layer(hidden)
        return output


class ModelTrainer():
    def __init__(self, model, criterion, optimizer):
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer

    def on_epoch_begin(self, is_train, name, batches_count):
        """
        Initializes metrics
        """
        self.epoch_loss = 0
        self.correct_count, self.total_count = 0, 0
        self.is_train = is_train
        self.name = name
        self.batches_count = batches_count

        self.model.train(is_train)

    def on_epoch_end(self):
        """
        Outputs final metrics
        """
        return '{:>5s} Loss = {:.5f}, Accuracy = {:.2%}'.format(
            self.name, self.epoch_loss / self.batches_count, self.correct_count / self.total_count
        )

    def on_batch(self, batch):
        """
        Performs forward and (if is_train) backward pass with optimization, updates metrics
        """
        logits = self.model(batch.tokens.transpose(0, 1))

        loss = self.criterion(logits, batch.label)

        predicted_label = logits.argmax(dim=1)

        self.total_count += predicted_label.size(0)
        self.correct_count += torch.sum(predicted_label == batch.label).item()

        if self.is_train:
            loss.backward()
            self.optimizer.step()
            self.optimizer.zero_grad()
        self.epoch_loss += loss.item()


def do_epoch(trainer, data_iter, is_train, name=None):
    trainer.on_epoch_begin(is_train, name, batches_count=len(data_iter))

    with torch.autograd.set_grad_enabled(is_train):
        with tqdm(total=trainer.batches_count) as progress_bar:
            for i, batch in enumerate(data_iter):
                batch_progress = trainer.on_batch(batch)

                progress_bar.update()
                progress_bar.set_description(batch_progress)

            epoch_progress = trainer.on_epoch_end()
            progress_bar.set_description(epoch_progress)
            progress_bar.refresh()


def fit(trainer, train_iter, epochs_count=1, val_iter=None):
    best_val_loss = None
    for epoch in range(epochs_count):
        name_prefix = '[{} / {}] '.format(epoch + 1, epochs_count)
        do_epoch(trainer, train_iter, is_train=True, name=name_prefix + 'Train:')

        if not val_iter is None:
            do_epoch(trainer, val_iter, is_train=False, name=name_prefix + '  Val:')


def run_on_test(trainer, test_iter):
    do_epoch(trainer, test_iter, is_train=False, name="Test:")
