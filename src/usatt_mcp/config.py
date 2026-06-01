import os
from dotenv import load_dotenv

load_dotenv()

USATT_USERNAME = os.environ.get("USATT_USERNAME", "")
USATT_PASSWORD = os.environ.get("USATT_PASSWORD", "")
SITE_BASE = "https://usatt.justgo.com"
API_BASE = "https://justgorestapi-prod-us.justgo.com"
TOURNAMENT_RESULT_TYPE_ID = "AA8491C6-C0EF-408E-9DE4-D141BCB42637"
