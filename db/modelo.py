import sqlite3

def conectar():
    return sqlite3.connect("db/tienda.db")

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            stock INTEGER,
            precio REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    cursor.execute("INSERT INTO productos (nombre, categoria, stock, precio) VALUES ('Cable coaxial', 'Cables', 25, 1200)")
    cursor.execute("INSERT INTO productos (nombre, categoria, stock, precio) VALUES ('Interruptor térmico', 'Protección', 10, 3500)")
    cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, contraseña) VALUES ('admin', '1234')")


    conn.commit()
    conn.close()

if __name__ == '__main__':
    crear_tablas()
