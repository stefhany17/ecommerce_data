# ETL de E-commerce: Centralización de Datos de Productos y Compras

## Descripción del proyecto
Este proyecto centraliza la información operativa de una empresa de e-commerce. Los datos provienen de una API externa que expone información de **productos** y **compras** en formato JSON.  

El flujo ETL (Extract, Transform, Load) incluye:  
- **Extracción:** Consumo de los endpoints `/products` y `/purchases`.  
- **Transformación:** Limpieza de datos, normalización de productos y expansión de compras por producto, incluyendo el cálculo de descuentos y totales por compra.  
- **Carga:** Inserción de los datos transformados en un Data Warehouse implementado en SQLite con un esquema relacional que facilita análisis posteriores.

---
## Stack tecnológico
- Lenguaje: Python 3.x
- Base de datos: SQLite
- Librerías: requests, datetime, collections, sqlite3
- Formato de datos: JSON

---

---

## Instrucciones de ejecución

- Clona el repositorio y entra en la carpeta del proyecto:

```bash
- git clone <URL_DEL_REPOSITORIO>
- cd <NOMBRE_DEL_PROYECTO>

- pip install -r requirements.txt

- Ejecuta el ETL. python main.py



## Arquitectura / Flujo ETL

  ┌─────────────┐
  │ API Externa │
  │ /products   │
  │ /purchases  │
  └─────┬───────┘
        │
        ▼
┌────────────────┐
│    Extract     │
│  extract.py    │
│ (requests)     │
└─────┬──────────┘
        │
        ▼
┌────────────────────────┐
│      Transform         │
│     transform.py       │
│ - Normaliza productos  │
│ - Expande compras      │
│ - Calcula descuentos   │
└─────┬──────────────────┘
        │
        ▼
┌────────────────────────┐
│         Load           │
│        load.py         │
│ - Inserta products     │
│ - Inserta purchases    │
│ - Inserta purchase_products │
│ (SQLite / Data Warehouse)   │
└─────┬──────────────────┘
        │
        ▼
  ┌─────────────┐
  │  Analítica  │
  │ Consultas / │
  │ Reportes    │
  └─────────────┘


.
├── main.py              # Orquestador ETL
├── extract.py           # Extracción de datos desde API
├── transform.py         # Transformación y limpieza de datos
├── load.py              # Inserción de datos en SQLite
├── config.py            # Configuración de endpoints y DB
├── requirements.txt     # Librerías necesarias
└── README.md


## Script para crear tablas de destino 

-- Tabla de productos
CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY,
    name        TEXT,
    description TEXT,
    price       REAL,
    category    TEXT,
    created_at  TEXT
);

-- Tabla de compras
CREATE TABLE IF NOT EXISTS purchases (
    id               TEXT PRIMARY KEY,
    status           TEXT,
    credit_card_type TEXT,
    purchase_date    TEXT,
    total            REAL
);

-- Tabla intermedia compras-productos
CREATE TABLE IF NOT EXISTS purchase_products (
    purchase_id TEXT,
    product_id  INTEGER,
    quantity    INTEGER,
    PRIMARY KEY (purchase_id, product_id),
    FOREIGN KEY (purchase_id) REFERENCES purchases(id),
    FOREIGN KEY (product_id)  REFERENCES products(id)
);



