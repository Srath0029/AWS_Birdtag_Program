# app/utils/logger.py
import os
import logging
import json
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


logger = logging.getLogger("birdtag-api")
logger.setLevel(logging.INFO)

log_handler = RotatingFileHandler(LOG_DIR, maxBytes=5*1024*1024, backupCount=3)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
