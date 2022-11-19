from dataset_extractor import create_dataset_iters
from lstm_model import DepressionClassifierModel, run_on_test
from model_train import start_training, init_trainer
from inference import infer


def main():
    tokens_field, train_iter, val_iter, test_iter = create_dataset_iters()
    model = DepressionClassifierModel(vocab_size=len(tokens_field.vocab))
    model_trainer = init_trainer(model)
    start_training(model_trainer, train_iter, val_iter)
    run_on_test(model_trainer, test_iter)
    infer('как же хочется сдохнуть я просто не могу так жить', model, tokens_field)
    infer('Играй в war thunder по ссылке в описании, вертолеты, танки, самолеты, тут все есть че тебе надо', model, tokens_field)
    infer('Я обожаю свою жизнь, как же хорошо жить на этом свете', model, tokens_field)
    infer('суицид - штука хорошая', model, tokens_field)
    infer('как же тяжело и больно', model, tokens_field)


if __name__ == "__main__":
    main()
