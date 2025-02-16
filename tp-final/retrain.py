import schedule
import time
from model import train_model
import os

def retrain():
    print("🔄 Réentraînement du modèle en cours...")
    try:
        train_model()
        print("✅ Modèle réentraîné avec succès.")
    except Exception as e:
        print(f"⚠️ Erreur lors du réentraînement : {e}")

schedule.every().week.do(retrain)

while True:
    schedule.run_pending()
    time.sleep(60) 
