import schedule
import time
from model import train_model

def retrain():
    print("Réentraînement du modèle...")
    train_model()

schedule.every().week.do(retrain)

while True:
    schedule.run_pending()
    time.sleep(3600)
