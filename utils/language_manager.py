
import os
import json
from utils.logger import logger

class LanguageManager:
    def __init__(self, base_path=None):
        if base_path is None:
            # Assuming the script is run from the project root
            self.base_path = os.path.join(os.getcwd(), 'locales')
        else:
            self.base_path = base_path
        self.supported_languages = ['en', 'fr', 'es', 'nl', 'de', 'it']
        self.default_language = 'en'

    def get_language_path(self, language):
        """
        Vérifie si la langue est supportée, sinon utilise la langue par défaut (en).
        Retourne le chemin du dossier de la langue.
        """
        logger.info(f"Requested language in LanguageManager: {language}")
        if language not in self.supported_languages:
            logger.warning(f"Unsupported language: {language}. Falling back to {self.default_language}")
            language = self.default_language
        path = os.path.join(self.base_path, language)
        logger.info(f"Using language path: {path}")
        return path

    def get_phase_descriptions(self, language):
        """
        Charge le fichier phase_descriptions.json pour la langue donnée
        """
        path = os.path.join(self.get_language_path(language), 'phase_descriptions.json')
        logger.info(f"Attempting to load phase descriptions from: {path}")
        data = self.load_json_file(path)
        logger.info(f"Loaded phase descriptions: {list(data.keys())}")
        return data

    def get_mantras(self, language):
        """
        Charge le fichier mantras.json pour la langue donnée.
        """
        path = os.path.join(self.get_language_path(language), 'mantras.json')
        logger.info(f"Attempting to load mantras from: {path}")
        data = self.load_json_file(path)
        logger.info(f"Loaded mantras: {list(data.keys())}")
        return data

    def load_json_file(self, file_path):
        """ 
        Charge un fichier JSON et gère les erreurs.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in file: {file_path}")
            return {}