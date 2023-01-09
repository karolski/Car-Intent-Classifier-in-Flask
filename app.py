import json

import nltk
from fuzzywuzzy import process
from joblib import load
import logging
import sys

from flask import Flask, request, jsonify
nltk.download('punkt')

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)
logging.info("app is running")


model = load("model.joblib")
vectorizer = load("vectorizer.joblib")
vocabulary = vectorizer.get_feature_names()

with open("make_and_model_clean.json", "r") as fp:
    make_and_model_list = json.load(fp)

def correct_phrase(phrase):
    tokens = nltk.word_tokenize(phrase)
    corrected_tokens = []
    for token in tokens:
        if token in vocabulary:
            corrected_tokens.append(token)
        else:
            extracted_token, match = process.extractOne(token, vocabulary)
            if match > 90:
                corrected_tokens.append(extracted_token)
    return " ".join(corrected_tokens)

@app.route("/", methods=["GET"])
def home():
    return """Welcome, go to <a href="/search?phrase=ferrari italia">search</a> to start."""

@app.route("/search", methods=["GET"])
def search():
    phrase = request.args.get("phrase")
    if not phrase:
        return jsonify({
            "message": "phrase parameter is required"
        }), 400

    corrected_phrase = correct_phrase(phrase)
    if not corrected_phrase:
        return jsonify({
            "message": "not found"
        }), 404

    logging.info(f"received phrase: {phrase}, corrected to {corrected_phrase}")

    feature_vector = vectorizer.transform([corrected_phrase])
    predicted_label_idx = model.predict(feature_vector)[0]
    make_and_model = make_and_model_list[predicted_label_idx]

    logging.info(f"found {make_and_model}")
    return jsonify({
        "make": make_and_model["make"],
        "model": make_and_model["model"]
    })