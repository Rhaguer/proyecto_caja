Haguermarket - README
Descripción
Haguermarket es una aplicación web desarrollada con Flask y MongoDB, diseñada para gestionar productos, ventas y carritos de compra en un entorno de negocio de barrio. La aplicación permite listar productos, agregar productos al carrito, gestionar el carrito de compras, procesar pagos y visualizar boletas de venta.

Requisitos Previos
Python 3.6 o superior
MongoDB
Instalación

1. Clonar el Repositorio
   bash
   Copiar código
   git clone https://github.com/tu-usuario/haguermarket.git
   cd haguermarket
2. Crear y Activar un Entorno Virtual
   bash
   Copiar código
   python -m venv venv
   source venv/bin/activate # En Windows usa `venv\Scripts\activate`
3. Instalar Dependencias
   bash
   Copiar código
   pip install -r requirements.txt
4. Configurar la Base de Datos MongoDB
   Asegúrate de tener MongoDB instalado y en ejecución. La configuración de la base de datos se encuentra en el archivo app.py:

python
Copiar código
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['cajaregistradora']
coleccion_productos = db['productos']
coleccion_carrito = db['carrito']
coleccion_ventas = db['ventas'] 5. Ejecutar la Aplicación
bash
Copiar código
python app.py 6. Abrir en el Navegador
Abre tu navegador y navega a http://127.0.0.1:5000 para ver la aplicación en acción.

Estructura del Proyecto
app.py: Archivo principal de la aplicación que contiene la configuración y las rutas.
templates/: Carpeta que contiene las plantillas HTML para las diferentes páginas de la aplicación.
static/: Carpeta que contiene archivos estáticos como CSS, JavaScript e imágenes.
Rutas Principales
/: Página principal.
/listar_productos: Listado de productos con paginación.
/carrito: Vista del carrito de compras.
/agregar_al_carrito/<int:id>: Ruta para agregar un producto al carrito.
/quitar_del_carrito/<string:id>: Ruta para quitar un producto del carrito.
/procesar_pago: Procesar el pago y generar una boleta de venta.
/boleta: Vista de la boleta de venta.
/nuevo: Formulario para crear un nuevo producto.
/crear_producto: Procesar la creación de un nuevo producto.
/contacto: Página de contacto.
Explicación de las Plantillas HTML
index.html
La página principal de la aplicación. Muestra un resumen o bienvenida al usuario.

listar.html
Esta página muestra una lista de productos con paginación. Los productos se obtienen desde la colección productos en MongoDB y se muestran con detalles como nombre, descripción, categoría, precio, stock y una imagen.

carrito.html
Muestra los productos agregados al carrito de compras, incluyendo detalles como nombre, cantidad, precio y subtotal. También se muestra el total de la compra y opciones para procesar el pago o quitar productos del carrito.

boleta.html
Después de procesar una compra, esta página muestra la boleta de venta con los detalles de los productos comprados, el total de la compra y la fecha de la transacción.

nuevo.html
Formulario para agregar un nuevo producto a la base de datos. Incluye campos para el nombre del producto, descripción, categorías, unidad de medida, valor de conversión, precio, stock inicial, stock actual y una URL para la imagen del producto.

contacto.html
Página de contacto que proporciona información sobre cómo comunicarse con los desarrolladores o el soporte de la aplicación.

Funcionalidades
Listar Productos
La ruta /listar_productos permite visualizar una lista de productos con soporte para paginación. Los productos se obtienen desde la colección productos en MongoDB.

Carrito de Compras
La ruta /carrito muestra los productos agregados al carrito, calculando el total de la compra. Se pueden agregar y quitar productos del carrito utilizando las rutas /agregar_al_carrito/<int:id> y /quitar_del_carrito/<string:id> respectivamente.

Procesar Pago
La ruta /procesar_pago calcula el total de la compra, actualiza el stock de los productos comprados y vacía el carrito. También registra la venta en la colección ventas.

Crear Producto
La ruta /crear_producto permite crear un nuevo producto y agregarlo a la colección productos.

Filtros de Plantilla
join_comma: Junta una lista de valores separados por comas.
format_currency: Formatea un número como una moneda.
Contribuciones
Las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna sugerencia, por favor abre un issue o envía un pull request.

Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.

¡Gracias por usar Haguermarket! Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.
