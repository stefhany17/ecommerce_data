# load.py
import sqlite3
from config import DB_PATH


def crear_tablas():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY,
            name        TEXT,
            description TEXT,
            price       REAL,
            category    TEXT,
            created_at  TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id               TEXT PRIMARY KEY,
            status           TEXT,
            credit_card_type TEXT,
            purchase_date    TEXT,
            total            REAL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS purchase_products (
            purchase_id TEXT,
            product_id  INTEGER,
            quantity    INTEGER,
            PRIMARY KEY (purchase_id, product_id),
            FOREIGN KEY (purchase_id) REFERENCES purchases(id),
            FOREIGN KEY (product_id)  REFERENCES products(id)
        );
    """)

    conn.commit()
    conn.close()


def insertar_products(products):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executemany("""
        INSERT OR REPLACE INTO products (id, name, description, price, category, created_at)
        VALUES (?, ?, ?, ?, ?, ?);
    """, [
        (
            p["id"],
            p["name"],
            p["description"],
            p["price"],
            p["category"],
            p["createdAt"],
        )
        for p in products
    ])

    conn.commit()
    conn.close()


def insertar_purchases(purchases, totales_por_compra):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executemany("""
        INSERT OR REPLACE INTO purchases (id, status, credit_card_type, purchase_date, total)
        VALUES (?, ?, ?, ?, ?);
    """, [
        (
            pur["id"],
            pur["status"],
            pur["creditCardType"],
            pur["purchaseDate"],
            totales_por_compra.get(pur["id"]),
        )
        for pur in purchases
    ])

    conn.commit()
    conn.close()


def insertar_purchase_products(filas_expand):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executemany("""
        INSERT OR REPLACE INTO purchase_products (purchase_id, product_id, quantity)
        VALUES (?, ?, ?);
    """, [
        (
            fila["purchase_id"],
            fila["product_id"],
            fila["quantity"]
        )
        for fila in filas_expand
    ])

    conn.commit()
    conn.close()