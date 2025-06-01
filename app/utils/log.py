# app/utils/log.py

import logging
import datetime
import os
from typing import Literal
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "log"

log_file = os.path.join(LOG_DIR, f"{datetime.datetime.now().strftime('%Y-%m-%d')}.log")
logging.basicConfig(level = logging.INFO,
                    format = "%(asctime)s - %(levelname)s: %(message)s",
                    handlers = [logging.FileHandler(log_file, encoding = "utf-8"), logging.StreamHandler()])
log = logging.getLogger(__name__)

def write(message: str, level = Literal["info", "warning", "error"]) :
    if level == "info" :
        logging.info(message)
    elif level == "warning" :
        logging.warning(message)
    elif level == "error" :
        logging.error(message)