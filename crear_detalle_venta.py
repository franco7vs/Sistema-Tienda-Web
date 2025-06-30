import sqlite3

conn = sqlite3.connect("db/tienda.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_venta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
""")

conn.commit()
conn.close()

print("Tabla 'detalle_venta' creada o ya existía.")
