# Utilisation d'une image Python officielle
FROM python:3.9

# Définition du répertoire de travail
WORKDIR /app

# Installer MySQL client pour interagir avec la base de données
RUN apt-get update && apt-get install -y default-mysql-client

# Copier les fichiers nécessaires
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py db.py /app/

# Exposer le port pour Flask
EXPOSE 5000

# Démarrer l'initialisation de la base de données et l'API
CMD ["/app/entrypoint-docker.sh"]

