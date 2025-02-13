#!/bin/bash

echo "⏳ Attente de la base de données MySQL..."
until mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" &> /dev/null; do
  sleep 2
done

echo "✅ Base de données MySQL prête."

echo "🚀 Initialisation de la base de données..."
mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" < /app/init_db.sql

echo "📊 Entraînement initial du modèle..."
python model.py

echo "🔥 Lancement de l'API Flask..."
exec python app.py
