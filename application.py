from flask import Flask, render_template, request, redirect
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave-secreta'  # Usada para manejar sesiones


def obtener_productos():
    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, categoria, stock, precio FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos


@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect('/login')
    ultimas_ventas = obtener_ultimas_ventas()
    return render_template('index.html', ultimas_ventas=ultimas_ventas)




@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/usuario')
def usuario():
    return render_template('usuario.html')

@app.route('/agregar-producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        stock = int(request.form['stock'])
        precio = float(request.form['precio'])

        conn = sqlite3.connect("db/tienda.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, categoria, stock, precio) VALUES (?, ?, ?, ?)",
                       (nombre, categoria, stock, precio))
        conn.commit()
        conn.close()

        return redirect('/productos')

    return render_template('agregar_producto.html')


@app.route('/eliminar-producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/productos')

@app.route('/editar-producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        stock = int(request.form['stock'])
        precio = float(request.form['precio'])

        cursor.execute("""
            UPDATE productos
            SET nombre = ?, categoria = ?, stock = ?, precio = ?
            WHERE id = ?
        """, (nombre, categoria, stock, precio, id))

        conn.commit()
        conn.close()
        return redirect('/productos')

    # GET: obtener datos actuales
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template('editar_producto.html', producto=producto)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        conn = sqlite3.connect("db/tienda.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", (usuario, contraseña))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['usuario'] = usuario
            return redirect('/')
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

@app.route('/productos')
def productos():
    if 'usuario' not in session:
        return redirect('/login')
    lista = obtener_productos()
    return render_template('productos.html', productos=lista)

@app.route('/sobre-nosotros')
def sobre_nosotros():
    return render_template('sobre_nosotros.html')


def obtener_clientes():
    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, telefono, direccion FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

@app.route('/clientes')
def clientes():
    if 'usuario' not in session:
        return redirect('/login')
    lista = obtener_clientes()
    return render_template('clientes.html', clientes=lista)

@app.route('/agregar-cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if 'usuario' not in session:
        return redirect('/login')

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        conn = sqlite3.connect("db/tienda.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, email, telefono, direccion) 
            VALUES (?, ?, ?, ?)
        """, (nombre, email, telefono, direccion))
        conn.commit()
        conn.close()

        return redirect('/clientes')

    return render_template('agregar_cliente.html')

@app.route('/editar-cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        cursor.execute("""
            UPDATE clientes
            SET nombre = ?, email = ?, telefono = ?, direccion = ?
            WHERE id = ?
        """, (nombre, email, telefono, direccion, id))
        conn.commit()
        conn.close()
        return redirect('/clientes')

    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/eliminar-cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/clientes')

def obtener_proveedores():
    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, telefono, direccion FROM proveedores")
    proveedores = cursor.fetchall()
    conn.close()
    return proveedores

@app.route('/proveedores')
def proveedores():
    if 'usuario' not in session:
        return redirect('/login')
    lista = obtener_proveedores()
    return render_template('proveedores.html', proveedores=lista)

@app.route('/agregar-proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    if 'usuario' not in session:
        return redirect('/login')

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        conn = sqlite3.connect("db/tienda.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proveedores (nombre, email, telefono, direccion) 
            VALUES (?, ?, ?, ?)
        """, (nombre, email, telefono, direccion))
        conn.commit()
        conn.close()

        return redirect('/proveedores')

    return render_template('agregar_proveedor.html')

@app.route('/editar-proveedor/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        cursor.execute("""
            UPDATE proveedores
            SET nombre = ?, email = ?, telefono = ?, direccion = ?
            WHERE id = ?
        """, (nombre, email, telefono, direccion, id))
        conn.commit()
        conn.close()
        return redirect('/proveedores')

    cursor.execute("SELECT * FROM proveedores WHERE id = ?", (id,))
    proveedor = cursor.fetchone()
    conn.close()
    return render_template('editar_proveedor.html', proveedor=proveedor)

@app.route('/eliminar-proveedor/<int:id>', methods=['POST'])
def eliminar_proveedor(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proveedores WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/proveedores')


from datetime import datetime

@app.route('/nueva-venta', methods=['GET', 'POST'])
def nueva_venta():
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    # Obtener clientes para el dropdown
    cursor.execute("SELECT id, nombre FROM clientes")
    clientes = cursor.fetchall()

    # Obtener productos para el dropdown (con stock > 0)
    cursor.execute("SELECT id, nombre, stock, precio FROM productos WHERE stock > 0")
    productos = cursor.fetchall()

    if request.method == 'POST':
        cliente_id = int(request.form['cliente'])
        productos_seleccionados = request.form.getlist('producto')
        cantidades = request.form.getlist('cantidad')

        # Validar que productos y cantidades coinciden
        if len(productos_seleccionados) != len(cantidades):
            conn.close()
            return "Error: Producto y cantidad no coinciden"

        total_venta = 0

        # Calcular total y verificar stock
        for i, prod_id in enumerate(productos_seleccionados):
            cursor.execute("SELECT stock, precio FROM productos WHERE id = ?", (prod_id,))
            stock, precio = cursor.fetchone()
            cant = int(cantidades[i])
            if cant > stock:
                conn.close()
                return f"Error: No hay suficiente stock para el producto ID {prod_id}"
            total_venta += cant * precio

        # Insertar la venta
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO ventas (cliente_id, fecha, total) VALUES (?, ?, ?)", (cliente_id, fecha, total_venta))
        venta_id = cursor.lastrowid

        # Insertar detalle y actualizar stock
        for i, prod_id in enumerate(productos_seleccionados):
            cant = int(cantidades[i])
            cursor.execute("SELECT precio FROM productos WHERE id = ?", (prod_id,))
            precio = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            """, (venta_id, prod_id, cant, precio))

            # Actualizar stock
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cant, prod_id))

        conn.commit()
        conn.close()

        return redirect('/ventas')

    conn.close()
    return render_template('nueva_venta.html', clientes=clientes, productos=productos)

@app.route('/ventas')
def ventas():
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    # Consultar ventas con datos de clientes
    cursor.execute("""
        SELECT ventas.id, clientes.nombre, ventas.fecha, ventas.total
        FROM ventas
        JOIN clientes ON ventas.cliente_id = clientes.id
        ORDER BY ventas.fecha DESC
    """)
    lista_ventas = cursor.fetchall()
    conn.close()
    return render_template('ventas.html', ventas=lista_ventas)

@app.route('/nueva-compra', methods=['GET', 'POST'])
def nueva_compra():
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre FROM proveedores")
    proveedores = cursor.fetchall()

    cursor.execute("SELECT id, nombre, stock, precio FROM productos")
    productos = cursor.fetchall()

    if request.method == 'POST':
        proveedor_id = int(request.form['proveedor'])
        productos_seleccionados = request.form.getlist('producto')
        cantidades = request.form.getlist('cantidad')
        precios_unitarios = request.form.getlist('precio_unitario')

        total_compra = 0

        for i in range(len(productos_seleccionados)):
            cant = int(cantidades[i])
            precio = float(precios_unitarios[i])
            total_compra += cant * precio

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO compras (proveedor_id, fecha, total) VALUES (?, ?, ?)",
                       (proveedor_id, fecha, total_compra))
        compra_id = cursor.lastrowid

        for i in range(len(productos_seleccionados)):
            prod_id = int(productos_seleccionados[i])
            cant = int(cantidades[i])
            precio = float(precios_unitarios[i])

            cursor.execute("""
                INSERT INTO detalle_compra (compra_id, producto_id, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
            """, (compra_id, prod_id, cant, precio))

            cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cant, prod_id))

        conn.commit()
        conn.close()

        return redirect('/compras')

    conn.close()
    return render_template('nueva_compra.html', proveedores=proveedores, productos=productos)

@app.route('/compras')
def compras():
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT compras.id, proveedores.nombre, compras.fecha, compras.total
        FROM compras
        JOIN proveedores ON compras.proveedor_id = proveedores.id
        ORDER BY compras.fecha DESC
    """)
    lista = cursor.fetchall()
    conn.close()

    return render_template('compras.html', compras=lista)

@app.route('/reportes')
def reportes():
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    # Total de ventas por fecha
    cursor.execute("""
        SELECT DATE(fecha), SUM(total)
        FROM ventas
        GROUP BY date(fecha)
    """)
    ventas_por_dia = cursor.fetchall()

    # Total de compras por fecha
    cursor.execute("""
        SELECT DATE(fecha), SUM(total)
        FROM compras
        GROUP BY date(fecha)
    """)
    compras_por_dia = cursor.fetchall()

    # Producto más vendido
    cursor.execute("""
        SELECT productos.nombre, SUM(detalle_venta.cantidad) as total_vendido
        FROM detalle_venta
        JOIN productos ON detalle_venta.producto_id = productos.id
        GROUP BY detalle_venta.producto_id
        ORDER BY total_vendido DESC
        LIMIT 1
    """)
    producto_top = cursor.fetchone()

    # Cliente con más compras
    cursor.execute("""
        SELECT clientes.nombre, COUNT(ventas.id) as cantidad
        FROM ventas
        JOIN clientes ON ventas.cliente_id = clientes.id
        GROUP BY cliente_id
        ORDER BY cantidad DESC
        LIMIT 1
    """)
    mejor_cliente = cursor.fetchone()

    # Proveedor con más compras
    cursor.execute("""
        SELECT proveedores.nombre, COUNT(compras.id) as cantidad
        FROM compras
        JOIN proveedores ON compras.proveedor_id = proveedores.id
        GROUP BY proveedor_id
        ORDER BY cantidad DESC
        LIMIT 1
    """)
    mejor_proveedor = cursor.fetchone()

    conn.close()

    return render_template(
        'reportes.html',
        ventas_por_dia=ventas_por_dia,
        compras_por_dia=compras_por_dia,
        producto_top=producto_top,
        mejor_cliente=mejor_cliente,
        mejor_proveedor=mejor_proveedor
    )

@app.route('/detalle-venta/<int:id>')
def detalle_venta(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    # Info general de la venta
    cursor.execute("""
        SELECT ventas.id, clientes.nombre, ventas.fecha, ventas.total
        FROM ventas
        JOIN clientes ON ventas.cliente_id = clientes.id
        WHERE ventas.id = ?
    """, (id,))
    venta = cursor.fetchone()

    # Detalle: productos vendidos
    cursor.execute("""
        SELECT productos.nombre, detalle_venta.cantidad, detalle_venta.precio_unitario
        FROM detalle_venta
        JOIN productos ON detalle_venta.producto_id = productos.id
        WHERE detalle_venta.venta_id = ?
    """, (id,))
    detalles = cursor.fetchall()

    conn.close()
    return render_template('detalle_venta.html', venta=venta, detalles=detalles)

@app.route('/detalle-compra/<int:id>')
def detalle_compra(id):
    if 'usuario' not in session:
        return redirect('/login')

    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()

    # Info general de la compra
    cursor.execute("""
        SELECT compras.id, proveedores.nombre, compras.fecha, compras.total
        FROM compras
        JOIN proveedores ON compras.proveedor_id = proveedores.id
        WHERE compras.id = ?
    """, (id,))
    compra = cursor.fetchone()

    # Detalle: productos comprados
    cursor.execute("""
        SELECT productos.nombre, detalle_compra.cantidad, detalle_compra.precio_unitario
        FROM detalle_compra
        JOIN productos ON detalle_compra.producto_id = productos.id
        WHERE detalle_compra.compra_id = ?
    """, (id,))
    detalles = cursor.fetchall()

    conn.close()
    return render_template('detalle_compra.html', compra=compra, detalles=detalles)

def obtener_ultimas_ventas(limit=5):
    conn = sqlite3.connect("db/tienda.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ventas.id, clientes.nombre, ventas.fecha, ventas.total
        FROM ventas
        JOIN clientes ON ventas.cliente_id = clientes.id
        ORDER BY ventas.fecha DESC
        LIMIT ?
    """, (limit,))
    ventas = cursor.fetchall()
    conn.close()
    return ventas


if __name__ == '__main__':
    app.run()

