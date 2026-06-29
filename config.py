import os
from dotenv import load_dotenv

load_dotenv()

SMARTSHEET_TOKEN = os.getenv("SMARTSHEET_API_TOKEN")
SMARTSHEET_SHEET_ID = os.getenv("SMARTSHEET_SHEET_ID")
SECRET_KEY = os.getenv("APP_SECRET_KEY")

IBGE_API_BASE = "https://servicodados.ibge.gov.br/api/v1"
