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
    # 1. Extraer
    products_api = consumir_products()
    purchases_api = consumir_purchases()

    # 2) Transformar
    products = transformar_products(products_api)
    purchases = transformar_purchases(purchases_api)

    products_by_id = construir_mapa_productos(products)
    filas_expand = expandir_compras(purchases, products_by_id)
    totales_por_compra = calcular_totales_por_compra(filas_expand)

    # 2.1 Preguntas

    print("\nCantidad de productos por compra:")
    for fila in filas_expand[:10]:
        print("Compra:", fila["purchase_id"])
        print("Producto:", fila["product_id"])
        print("Nombre:", fila["product_name"])
        print("Cantidad:", fila["quantity"])
        print("Total línea (con descuento):", fila["total_linea"])
        print("---")

    print("\nTotal por compra (con descuentos aplicados):")
    contador = 0
    for purchase_id, total in totales_por_compra.items():
        print("Compra:", purchase_id, "Total:", total)
        contador += 1
        if contador == 10:
            break

    # 3) Load
    crear_tablas()
    insertar_products(products)
    insertar_purchases(purchases, totales_por_compra)
    insertar_purchase_products(filas_expand)



    print("\nETL completado.")


