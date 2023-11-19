import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()


API_TOKEN = os.environ.get("API_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

logger.debug(f"API_TOKEN={API_TOKEN},WEBHOOK_URL={WEBHOOK_URL}")