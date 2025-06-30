import sqlite3

conn = sqlite3.connect("db/tienda.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proveedor_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
)
""")

conn.commit()
conn.close()

print("Tabla 'compras' creada o ya existía.")
