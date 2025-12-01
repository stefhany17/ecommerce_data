# extract.py Extraccion - consumir el API
import requests
from config import URL_PRODUCTS, URL_PURCHASES, HEADERS

def consumir_products():
    resp = requests.get(URL_PRODUCTS, headers=HEADERS)

    if resp.status_code != 200:
        print("Error al consumir /api/products:", resp.status_code, resp.text)
        return []

    data = resp.json()
    return data["data"]


def consumir_purchases():
    resp = requests.get(URL_PURCHASES, headers=HEADERS)

    if resp.status_code != 200:
        print("Error al consumir /api/purchases:", resp.status_code, resp.text)
        return []

    data = resp.json()
    return data["data"]