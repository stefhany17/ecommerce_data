# transform.py
from datetime import datetime
from collections import Counter



# Products

def transformar_products(productos_api):
    productos_transformados = []

    for p in productos_api:
        pid = p.get("id")
        name = (p.get("name") or "").strip()
        description = (p.get("description") or "").strip()
        category = (p.get("category") or "").strip()
        created_at_str = p.get("createdAt")


        try:
            price = float(p.get("price"))
        except (TypeError, ValueError):
            price = None

        productos_transformados.append({
            "id": pid,
            "name": name,
            "description": description,
            "price": price,
            "category": category,
            "createdAt": created_at_str,
        })

    return productos_transformados


# Purchases

def transformar_purchases(purchases_api):
    purchases_transformadas = []

    for purchase in purchases_api:
        pid = purchase.get("id")
        status = (purchase.get("status") or "").strip()
        cc_type = (purchase.get("creditCardType") or "").strip()
        cc_number = (purchase.get("creditCardNumber") or "").strip()
        # Purchase date string
        purchase_date_str = purchase.get("purchaseDate")

        # Conversión de fecha
        purchase_date_dt = None
        if purchase_date_str:
            try:
                purchase_date_dt = datetime.strptime(purchase_date_str, "%m/%d/%Y")
            except ValueError:
                purchase_date_dt = None

        # Lista de productos en la compra
        productos = purchase.get("products", [])

        purchases_transformadas.append({
            "id": pid,
            "status": status,
            "creditCardType": cc_type,
            "creditCardNumber": cc_number,
            "purchaseDate": purchase_date_str,
            "purchaseDate_dt": purchase_date_dt,
            "products": productos,
        })

    return purchases_transformadas



# Metodos

def construir_mapa_productos(products):
    return {p["id"]: p for p in products}


def expandir_compras(purchases, products_by_id):
    filas = []

    for pur in purchases:
        purchase_id = pur["id"]
        purchase_date = pur["purchaseDate"]
        status = pur["status"]
        productos_compra = pur.get("products", [])

        # Cantidad comprada por producto
        ids = [item["id"] for item in productos_compra]
        cantidades = Counter(ids)

        for product_id, quantity in cantidades.items():
            prod = products_by_id.get(product_id)

            if prod is None:
                name = None
                category = None
                unit_price = 0.0
            else:
                name = prod["name"]
                category = prod["category"]
                unit_price = float(prod["price"]) if prod["price"] is not None else 0.0

            item_ejemplo = next(
                (it for it in productos_compra if it["id"] == product_id),
                None
            )
            discount = item_ejemplo.get("discount", 0) if item_ejemplo else 0
            price_after_discount = unit_price * (1 - discount / 100.0)
            total_linea = price_after_discount * quantity

            filas.append({
                "purchase_id": purchase_id,
                "purchase_date": purchase_date,
                "status": status,
                "product_id": product_id,
                "product_name": name,
                "product_category": category,
                "unit_price": unit_price,
                "discount_percent": discount,
                "quantity": quantity,
                "total_linea": round(total_linea, 2),
            })

    return filas



def calcular_totales_por_compra(filas_expand):
    totales = {}

    for fila in filas_expand:
        purchase_id = fila["purchase_id"]
        total_linea = fila["total_linea"]

        totales[purchase_id] = totales.get(purchase_id, 0.0) + total_linea

    result = {}
    for purchase_id, total in totales.items():
        result[purchase_id] = round(total, 2)

    return result