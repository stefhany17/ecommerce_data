# transform.py
from datetime import datetime
from collections import Counter


# -----------------------------
# Products
# -----------------------------
def transformar_products(raw_products):
    productos_transformados = []

    for p in raw_products:
        pid = p.get("id")
        name = (p.get("name") or "").strip()
        description = (p.get("description") or "").strip()
        category = (p.get("category") or "").strip()
        created_at_str = p.get("createdAt")

        price_raw = p.get("price")
        try:
            price = float(price_raw)
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


# -----------------------------
# Purchases
# -----------------------------
def transformar_purchases(raw_purchases):
    compras_transformadas = []

    for pur in raw_purchases:
        pid = pur.get("id")
        status = (pur.get("status") or "").strip()
        cc_type = (pur.get("creditCardType") or "").strip()
        cc_number = (pur.get("creditCardNumber") or "").strip()
        purchase_date_str = pur.get("purchaseDate")

        purchase_date_dt = None
        if purchase_date_str:
            try:
                purchase_date_dt = datetime.strptime(purchase_date_str, "%m/%d/%Y")
            except ValueError:
                purchase_date_dt = None

        products_list = pur.get("products", [])

        compras_transformadas.append({
            "id": pid,
            "status": status,
            "creditCardType": cc_type,
            "creditCardNumber": cc_number,
            "purchaseDate": purchase_date_str,
            "purchaseDate_dt": purchase_date_dt,
            "products": products_list,
        })

    return compras_transformadas


# -----------------------------
# Helpers para análisis
# -----------------------------
def construir_mapa_productos(products):
    return {p["id"]: p for p in products}


def expandir_compras(purchases, products_by_id):
    filas = []

    for pur in purchases:
        purchase_id = pur["id"]
        purchase_date = pur["purchaseDate"]
        status = pur["status"]
        productos_compra = pur.get("products", [])

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
        pid = fila["purchase_id"]
        totales[pid] = totales.get(pid, 0.0) + fila["total_linea"]
    return {pid: round(total, 2) for pid, total in totales.items()}