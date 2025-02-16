from flask import Flask, request, jsonify
import joblib
import numpy as np
from db import get_db_connection
from model import preprocess_text, predict_sentiment

app = Flask(__name__)

# Chargement du modèle et du vectorizer
try:
    vectorizer, model_positive = joblib.load("model.pkl")
    print("✅ Modèle chargé avec succès.")
except FileNotFoundError:
    print("⚠️ Modèle non trouvé. Veuillez entraîner le modèle d'abord.")
    vectorizer, model_positive = None, None, None
except Exception as e:
    print(f"⚠️ Erreur lors du chargement du modèle : {e}")
    vectorizer, model_positive = None, None, None

def store_tweet_in_db(tweet, score):
    if score > 0:
        positive, negative = 1, 0
    else:
        positive, negative = 0, 1

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
            (tweet, positive, negative),
        )
        conn.commit()
        print(f"✅ Tweet enregistré: {tweet} | Score: {score} | Positif: {positive}, Négatif: {negative}")

    except Exception as err:
        print(f"⚠️ Erreur MySQL lors de l'insertion : {err}")

    finally:
        cursor.close()
        conn.close()

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    global vectorizer, model_positive

    # Vérification si le modèle est bien chargé
    if any(var is None for var in [vectorizer, model_positive]):
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
