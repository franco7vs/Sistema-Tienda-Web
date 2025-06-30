import sqlite3

conn = sqlite3.connect("db/tienda.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compra_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    FOREIGN KEY (compra_id) REFERENCES compras(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
""")

conn.commit()
conn.close()

print("Tabla 'detalle_compra' creada o ya existía.")
