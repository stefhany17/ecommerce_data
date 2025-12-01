# extract.py
import requests
from config import URL_PRODUCTS, URL_PURCHASES, HEADERS


def consumir_products():
    resp = requests.get(URL_PRODUCTS, headers=HEADERS)
    if not resp.ok:
        print("Error al consumir /api/products:", resp.status_code, resp.text)
        return []
    data = resp.json()        # dict con keys: "data", "timestamp"
    return data["data"]       # lista de Product crudos


def consumir_purchases():
    resp = requests.get(URL_PURCHASES, headers=HEADERS)
    if not resp.ok:
        print("Error al consumir /api/purchases:", resp.status_code, resp.text)
        return []
    data = resp.json()        # dict con keys: "data", "timestamp"
    return data["data"]       # lista de Purchase crudos