from flask import Flask, jsonify, request
from transformers import pipeline

app = Flask(__name__)
classifier = pipeline("text-classification", model="/home/dell/Документы/checkpoint-24528")


# API /health - Check if app is running
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"App": "OK"})


# API /predict -  Prediction of model
@app.route('/predict', methods=['POST'])
def predict():
    global classifier
    try:
        message_to_predict = request.get_json()
        result = classifier(message_to_predict['text'])[0]
        return jsonify(result)
    except Exception as e:
        print("Error: Issue with prediction.", e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=44444, debug=True)
