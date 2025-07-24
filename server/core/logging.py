"""
Loguru logging configuration for Django.
Simple, clean setup with colors and daily rotation.
"""

import os
import sys
from loguru import logger

def setup_logging():
    from core.settings import BASE_DIR
    """Configure loguru for Django with colors and rotation."""
    
    # Remove default logger
    logger.remove()
    
    # Get environment settings
    environment = os.getenv("ENVIRONMENT", "development")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Use /app/logs inside server directory 
    
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    
    if environment == "development":
        # Development: colorful console + debug file
        logger.add(
            sys.stdout,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}:{line}</cyan> | <level>{message}</level>",
            level=log_level,
            colorize=True,
        )
        
        logger.add(
            log_dir / "debug.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} | {message}",
            level=log_level,
            rotation="00:00",  # Daily rotation
            retention="7 days",
            compression="zip",
        )
    else:
        # Production: structured console + application file
        logger.add(
            sys.stdout,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} | {message}",
            level=log_level,
            colorize=False,
        )
        
        logger.add(
            log_dir / "application.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} | {message}",
            level=log_level,
            rotation="100 MB",
            retention="30 days",
            compression="gz",
        )

# Intercept Django's logging and redirect to Loguru
import logging

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == __file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())