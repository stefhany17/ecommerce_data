# main.py
from pprint import pprint

from extract import consumir_products, consumir_purchases
from transform import (
    transformar_products,
    transformar_purchases,
    construir_mapa_productos,
    expandir_compras,
    calcular_totales_por_compra,
)
from load import (
    crear_tablas,
    insertar_products,
    insertar_purchases,
    insertar_purchase_products,
)


if __name__ == "__main__":
    # 1) Extract
    raw_products = consumir_products()
    raw_purchases = consumir_purchases()

    # 2) Transform
    products = transformar_products(raw_products)
    purchases = transformar_purchases(raw_purchases)

    products_by_id = construir_mapa_productos(products)
    filas_expand = expandir_compras(purchases, products_by_id)
    totales_por_compra = calcular_totales_por_compra(filas_expand)

    # 3) Load
    crear_tablas()
    insertar_products(products)
    insertar_purchases(purchases, totales_por_compra)
    insertar_purchase_products(filas_expand)

    # Impresiones que te interesaban
    print("\n=== Cantidad (quantity) de cada producto por compra ===")
    for fila in filas_expand[:10]:
        print(
            f"Compra {fila['purchase_id']} | "
            f"Producto {fila['product_id']} ({fila['product_name']}) | "
            f"Cantidad: {fila['quantity']} | "
            f"Total línea (con desc): {fila['total_linea']}"
        )

    print("\n=== Total por compra con descuentos aplicados ===")
    for purchase_id, total in list(totales_por_compra.items())[:10]:
        print(f"Compra {purchase_id} -> Total: {total}")

    print("\nETL completado.")


