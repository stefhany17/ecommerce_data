# config.py  - Archivo de configuracion

# Url base de la api
BASE_URL = "https://mnpwhdbcsk.us-east-2.awsapprunner.com"

# Endpoints necesarios
URL_PRODUCTS = f"{BASE_URL}/api/products"
URL_PURCHASES = f"{BASE_URL}/api/purchases"

#Utilizacion en el header de la api key dada
HEADERS = {
    "x-api-key": "8yBO1wKiiIbcBT0",
    "Accept": "application/json"
}

DB_PATH = "etl.db"