import os
from dotenv import load_dotenv
from pathlib import Path

# Obtenir le chemin absolu du répertoire contenant config.py
BASE_DIR = Path(__file__).resolve().parent

# Charger les variables d'environnement depuis le fichier config.env
load_dotenv(BASE_DIR / 'config.env')

# Configuration email
EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

# Configuration MongoDB
MONGO_URI = os.getenv('MONGO_URI')

# Configuration de notification
NOTIFICATION_EMAIL = os.getenv('NOTIFICATION_EMAIL')

# Affichage des valeurs chargées (à des fins de débogage)
if __name__ == "__main__":
    print(f"MONGO_URI chargé : {MONGO_URI}")
    print(f"NOTIFICATION_EMAIL chargé : {NOTIFICATION_EMAIL}")