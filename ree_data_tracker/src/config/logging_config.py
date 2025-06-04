import logging
import sys
from datetime import datetime
import os
from .tinybird_log_handler import TinybirdLogHandler

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Configure logging
def setup_logger(name, send_callback=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # File handler
    log_file = os.path.join(log_dir, f'ree_tracker_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Add Tinybird handler if callback is provided
    if send_callback:
        tinybird_handler = TinybirdLogHandler(level=logging.INFO, send_callback=send_callback)
        tinybird_handler.setFormatter(file_formatter)
        logger.addHandler(tinybird_handler)

    return logger 