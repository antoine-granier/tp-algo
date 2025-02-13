from flask import Flask, request, jsonify
import joblib
import numpy as np
import mysql.connector
from db import get_db_connection, create_table
from model import preprocess_text, predict_sentiment, train_model

app = Flask(__name__)

# Chargement du modèle et du vecteur
try:
    vectorizer, model_positive, model_negative = joblib.load("model.pkl")
    print("✅ Modèle chargé avec succès.")
except Exception as e:
    print(f"⚠️ Erreur lors du chargement du modèle : {e}")
    vectorizer, model_positive, model_negative = None, None, None

def store_tweet_in_db(tweet, score):
    """Stocke le tweet analysé dans MySQL avec les labels générés."""
    if score > 0.1:
        positive, negative = 1, 0
    elif score < -0.1:
        positive, negative = 0, 1
    else:
        positive, negative = 0, 0

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
            (tweet, positive, negative),
        )
        conn.commit()
        print(f"✅ Tweet enregistré: {tweet} | Score: {score} | Positif: {positive}, Négatif: {negative}")

    except mysql.connector.Error as err:
        print(f"⚠️ Erreur MySQL lors de l'insertion : {err}")

    finally:
        cursor.close()
        conn.close()

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    """Endpoint pour analyser les sentiments d'une liste de tweets."""
    global vectorizer, model_positive, model_negative

    # Vérification si le modèle est bien chargé
    if any(var is None for var in [vectorizer, model_positive, model_negative]):
        return jsonify({"error": "Modèle non chargé"}), 500

    try:
        data = request.json
        if not isinstance(data, list):
            raise ValueError("Format invalide, une liste de tweets est attendue.")

    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

    response = {}

    for tweet in data:
        if not isinstance(tweet, str) or not tweet.strip():
            response[tweet] = "Erreur : Tweet invalide"
            continue

        try:
            sentiment_score = predict_sentiment(tweet)
            response[tweet] = sentiment_score

            store_tweet_in_db(tweet, sentiment_score)

        except Exception as e:
            response[tweet] = f"Erreur : {str(e)}"

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
