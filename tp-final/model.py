import re
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv
import os
import mysql.connector

def preprocess_text(text):
    """Nettoie le texte en enlevant les caractères spéciaux et en mettant en minuscules."""
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text

def train_model(conn):
    """Entraîne un modèle de régression logistique sur les tweets stockés en base de données."""
    
    # Récupération des données depuis MySQL
    df = pd.read_sql("SELECT text, positive, negative FROM tweets", conn)
    
    # Nettoyage du texte
    df['processed_text'] = df['text'].apply(preprocess_text)

    # Vectorisation du texte
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(df['processed_text'])
    
    y_positive = df['positive']
    y_negative = df['negative']

    # Split des données pour les modèles positifs et négatifs
    X_train, X_test, y_train_positive, y_test_positive = train_test_split(
        X, y_positive, test_size=0.2, random_state=42
    )
    X_train, X_test, y_train_negative, y_test_negative = train_test_split(
        X, y_negative, test_size=0.2, random_state=42
    )

    # Entraînement des modèles
    model_positive = LogisticRegression()
    model_positive.fit(X_train, y_train_positive)
    y_pred_positive = model_positive.predict(X_test)

    model_negative = LogisticRegression()
    model_negative.fit(X_train, y_train_negative)
    y_pred_negative = model_negative.predict(X_test)

    # Évaluation des modèles
    accuracy_positive = accuracy_score(y_test_positive, y_pred_positive)
    accuracy_negative = accuracy_score(y_test_negative, y_pred_negative)

    # Sauvegarde du modèle
    with open('model.pkl', 'wb') as f:
        pickle.dump((vectorizer, model_positive, model_negative), f)

    print(f"Modèle entraîné avec succès !\n"
          f"Précision (positive): {accuracy_positive:.2f}\n"
          f"Précision (négative): {accuracy_negative:.2f}")

def predict_sentiment(tweet):
    """Prédit le sentiment d'un tweet donné entre -1 (négatif) et 1 (positif)."""
    
    # Charger le modèle entraîné
    with open('model.pkl', 'rb') as f:
        vectorizer, model_positive, model_negative = pickle.load(f)

    # Prétraitement du tweet
    tweet = preprocess_text(tweet)
    X = vectorizer.transform([tweet])

    # Prédictions des probabilités
    positive_score = model_positive.predict_proba(X)[0][1]
    negative_score = model_negative.predict_proba(X)[0][1]

    # Score de sentiment normalisé entre -1 et 1
    sentiment_score = round((positive_score - negative_score), 2)

    return sentiment_score

if __name__ == "__main__":
    # Establish MySQL connection
    try:
        # Load environment variables from .env file
        load_dotenv()

        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        print("✅ Connected to MySQL. Training model...")
        train_model(conn)
    except mysql.connector.Error as e:
        print(f"⚠️ MySQL Connection Error: {e}")
    finally:
        if conn:
            conn.close()

