# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

SMARTSHEET_TOKEN = "Rwrx12lpcpOPM0rauIyLf4k5izmwQmjsT8cc6"
SMARTSHEET_SHEET_ID = "3103817011777412"
SECRET_KEY = os.getenv("APP_SECRET_KEY", "chave_padrao_facilities")

IBGE_API_BASE = "https://servicodados.ibge.gov.br/api/v1"

PAINEL_SENHA = "BRMT_Facilities26"
