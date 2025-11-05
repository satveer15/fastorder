import logging
import sys

def setup_logging():
    """Configure logging for the application"""
    # Create logger
    logger = logging.getLogger("order_api")
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Add handler
    logger.addHandler(console_handler)

    return logger

# Create global logger instance
logger = setup_logging()
