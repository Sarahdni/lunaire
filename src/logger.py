import logging
import os


def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Exemple d'utilisation
# main_logger = setup_logger('main_logger', 'logs/main.log')
# main_logger.info('Ceci est un message de log')