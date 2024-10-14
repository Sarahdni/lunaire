import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='app.log', log_level=logging.INFO):
    """
    Set up and configure the logger for the application.

    Args:
    log_file (str): Name of the log file (default: 'app.log')
    log_level (int): Logging level (default: logging.INFO)

    Returns:
    logging.Logger: Configured logger object
    """
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    logger = logging.getLogger('cycle_sync_app')
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File handler (with rotation)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, log_file),
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create and configure the logger
logger = setup_logger()