# app.py
from flask import Flask, render_template, redirect, url_for, request, session, flash
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuración de la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['cajaregistradora']
coleccion_productos = db['productos']
coleccion_carrito = db['carrito']
coleccion_ventas = db['ventas']

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listar_productos')  
def listar_productos():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 12))

    pipeline = [
        {
            '$project': {
                'id': 1,
                'nombre': 1,
                'descripcion': 1,
                'categoria': 1,
                'unidadMedida': 1,
                'precio': 1,
                'stock': 1,
                'urlFoto': 1
            }
        },
        {'$skip': skip},
        {'$limit': limit},
    ]

    productos = list(coleccion_productos.aggregate(pipeline))
    total_productos = coleccion_productos.count_documents({})
    return render_template('listar.html', productos=productos, skip=skip, limit=limit, total_productos=total_productos)

# Funcionalidades de carrito y ventas
@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    pipeline = [
        {'$project': {
            'producto_id': 1,
            'nombre': 1,
            'cantidad': 1,
            'urlFoto': 1,
            'precio': 1,
            'subtotal': 1
        }}
    ]

    items = list(coleccion_carrito.aggregate(pipeline))
    total = sum(item['precio'] * item['cantidad'] for item in items)
    return render_template('carrito.html', productos=items, total=total)

@app.route('/agregar_al_carrito/<int:id>', methods=['POST'])
def agregar_al_carrito(id):
    cantidad = int(request.form['cantidad'])
    
    # Buscar el producto en la colección de productos
    pipeline = [
        {'$match': {'id': id}},
        {'$project': {
            'id': 1,
            'nombre': 1,
            'precio': 1,
            'urlFoto': 1
        }}
    ]

    producto = list(coleccion_productos.aggregate(pipeline))
    if producto:
        producto = producto[0]  
        
        pipeline = [
            {'$match': {'producto_id': id}},
            {'$project': {
                'producto_id': 1,
                'nombre': 1,
                'cantidad': 1,
                'urlFoto': 1,
                'precio': 1,
                'subtotal': 1
            }}
        ]
        
        carrito_item = list(coleccion_carrito.aggregate(pipeline))

        if carrito_item:
            carrito_item = carrito_item[0]
            # Si el producto ya existe en el carrito, actualizar la cantidad y el subtotal
            nueva_cantidad = carrito_item['cantidad'] + cantidad
            nuevo_subtotal = producto['precio'] * nueva_cantidad
            
            coleccion_carrito.update_one(
                {'producto_id': producto['id']},
                {'$set': {'cantidad': nueva_cantidad, 'subtotal': nuevo_subtotal}}
            )
        else:
            # Si el producto no existe en el carrito, agregarlo
            item_carrito = {
                'producto_id': producto['id'],
                'nombre': producto['nombre'],
                'cantidad': cantidad,
                'urlFoto': producto['urlFoto'],
                'precio': producto['precio'],
                'subtotal': producto['precio'] * cantidad
            }
            
            coleccion_carrito.insert_one(item_carrito) 
    
    return redirect(url_for('listar_productos'))

@app.route('/quitar_del_carrito/<string:id>', methods=['POST'])
def quitar_del_carrito(id):
    try:
        id = ObjectId(id)
    except:
        pass

    coleccion_carrito.delete_one({'_id': id})
    
    return redirect(url_for('carrito'))

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    # Calcular el total usando una tubería de agregación
    pipeline = [
        {
            '$group': {
                '_id': None,
                'total': { '$sum': '$subtotal' }
            }
        }
    ]
    total_result = list(coleccion_carrito.aggregate(pipeline))
    total = total_result[0]['total'] if total_result else 0
    
    # Obtener los datos del carrito
    items = list(coleccion_carrito.find())
    
    # Reducir el stock de los productos comprados
    for item in items:
        producto_id = item['producto_id']
        cantidad_comprada = item['cantidad']
        coleccion_productos.update_one(
            {'id': producto_id},
            {'$inc': {'stock': -cantidad_comprada}}
        )
        
    venta = {
        "productos": items,
        "total": total,
        "fechaCreacion": datetime.now(), 
        "fechaActualizacion": datetime.now()  
    }
    
    coleccion_ventas.insert_one(venta)
    
    # Vaciar el carrito
    coleccion_carrito.delete_many({})
    
    return redirect(url_for('index'))

@app.route('/nuevo')
def nuevo():
    ultimo_producto = list(coleccion_productos.find().sort('id', -1).limit(1))
    if ultimo_producto:
        ultimo_id = int(ultimo_producto[0]['id'])
    else:
        ultimo_id = 0

    nuevo_id = ultimo_id + 1
    return render_template('nuevo.html', nuevo_id=nuevo_id)

@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    item = {
        "id": int(request.form['id']),  
        "nombre": request.form['nombre'],
        "descripcion": request.form['descripcion'],
        "categories": request.form['categories'].split(','),
        "unidadMedida": request.form['unidadMedida'],
        "valorConversion": int(request.form['valorConversion']),
        "precio": int(request.form['precio']),
        "stockInicial": int(request.form['stockInicial']),
        "stock": int(request.form['stock']),
        "urlFoto": request.form['urlFoto'],
        "fechaCreacion": datetime.now(),  
        "fechaActualizacion": datetime.now() 
    }
    print(item)
    coleccion_productos.insert_one(item)
    return redirect(url_for('index'))

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.template_filter('join_comma')
def join_comma(value):
    return ', '.join(value)

@app.template_filter('format_currency')
def format_currency(value, decimals=2):
    format_string = "{:,.{}f}".format(value, decimals)
    return format_string



if __name__ == '__main__':
    app.run(debug=True)
