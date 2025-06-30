import sqlite3

conn = sqlite3.connect("db/tienda.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
""")

conn.commit()
conn.close()

print("Tabla 'ventas' creada o ya existía.")
