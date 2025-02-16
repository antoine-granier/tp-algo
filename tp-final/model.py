import re
import joblib
import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sqlalchemy import create_engine
from dotenv import load_dotenv
from db import get_db_connection

load_dotenv()

def preprocess_text(text):
    """Nettoie le texte en enlevant les caractères spéciaux et en mettant en minuscules."""
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text.strip()

def train_model():
    """Entraîne un modèle de régression logistique sur les tweets stockés en base de données."""
    
    db_url = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)

    df = pd.read_sql("SELECT text, positive, negative FROM tweets", engine)

    if df.empty:
        print("⚠️ Aucune donnée disponible pour l'entraînement.")
        return
    
    # Nettoyage du texte
    df['processed_text'] = df['text'].apply(preprocess_text)

    # Vectorisation du texte
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
    X = vectorizer.fit_transform(df['processed_text'])
    
    y_positive = df['positive']

    if len(set(y_positive)) < 2:
        print("⚠️ Erreur : Les données contiennent une seule classe. Ajoutez plus d'exemples.")
        return

    # Split des données
    X_train, X_test, y_train_positive, y_test_positive = train_test_split(X, y_positive, test_size=0.2, random_state=42)

    # Entraînement des modèles
    model_positive = LogisticRegression(max_iter=1000, solver='lbfgs')

    model_positive.fit(X_train, y_train_positive)

    # Prédictions et évaluation
    y_pred_positive = model_positive.predict(X_test)

    accuracy_positive = accuracy_score(y_test_positive, y_pred_positive)

    # Sauvegarde
    joblib.dump((vectorizer, model_positive), "model.pkl")

    print(f"✅ Modèle entraîné avec succès !\n"
          f"📊 Précision (positive): {accuracy_positive:.2f}\n")

def predict_sentiment(tweet):
    """Prédit le sentiment d'un tweet donné entre -1 (négatif) et 1 (positif)."""
    
    # Charger le modèle entraîné
    try:
        vectorizer, model_positive = joblib.load("model.pkl")
    except FileNotFoundError:
        print("⚠️ Modèle non trouvé. Veuillez entraîner le modèle d'abord.")
        return None

    # Prétraitement du tweet
    tweet = preprocess_text(tweet)
    X = vectorizer.transform([tweet])

    # Prédictions des probabilités
    positive_score = model_positive.predict_proba(X)[0][1]

    # Score de sentiment normalisé entre -1 et 1
    sentiment_score = 2 * positive_score - 1

    return sentiment_score

if __name__ == "__main__":
    try:
        print("🔄 Connexion à MySQL pour l'entraînement du modèle...")
        train_model()
    except Exception as e:
        print(f"⚠️ Erreur pendant l'entraînement du modèle : {e}")
