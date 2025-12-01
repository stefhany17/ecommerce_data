# config.py
BASE_URL = "https://mnpwhdbcsk.us-east-2.awsapprunner.com"
URL_PRODUCTS = f"{BASE_URL}/api/products"
URL_PURCHASES = f"{BASE_URL}/api/purchases"

HEADERS = {
    "x-api-key": "8yBO1wKiiIbcBT0",
    "Accept": "application/json"
}

DB_PATH = "etl.db"