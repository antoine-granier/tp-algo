import mysql.connector
import os
import time

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "sentiment_db")

def get_db_connection():
    """Établit une connexion à la base de données MySQL."""
    while True:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            print("✅ Connexion MySQL réussie !")
            return conn
        except mysql.connector.Error as err:
            print(f"⚠️ Erreur de connexion MySQL : {err}")
            print("🔄 Nouvelle tentative dans 5 secondes...")
            time.sleep(5)

def create_table():
    """Crée la table `tweets` si elle n'existe pas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text TEXT NOT NULL,
            positive INT NOT NULL,
            negative INT NOT NULL
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Table `tweets` vérifiée/créée.")

if __name__ == "__main__":
    create_table()
