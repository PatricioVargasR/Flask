import requests

# URL de la API de GitHub y el repositorio que deseas eliminar
url = 'https://api.github.com/repos/tu_usuario/tu_repositorio'

# Encabezados con el token de autenticación (necesitas reemplazar 'TU_TOKEN' con tu token real)
headers = {
    'Authorization': 'token TU_TOKEN'
}

# Realiza la solicitud DELETE
response = requests.delete(url, headers=headers)

# Verifica el código de estado de la respuesta
if response.status_code == 204:
    print('El repositorio ha sido eliminado exitosamente.')
else:
    print(f'Error al eliminar el repositorio. Código de estado: {response.status_code}')
    print('Respuesta del servidor:', response.text)


import requests

# URL de la API de GitHub y el repositorio que deseas actualizar
url = 'https://api.github.com/repos/tu_usuario/tu_repositorio'

# Encabezados con el token de autenticación (necesitas reemplazar 'TU_TOKEN' con tu token real)
headers = {
    'Authorization': 'token TU_TOKEN',
    'Accept': 'application/vnd.github.v3+json'  # Especifica el formato de respuesta deseado
}

# Datos que deseas actualizar en el repositorio
data = {
    'description': 'Nueva descripción para el repositorio'
}

# Realiza la solicitud PUT para actualizar la descripción del repositorio
response = requests.put(url, headers=headers, json=data)

# Verifica el código de estado de la respuesta
if response.status_code == 200:
    print('La descripción del repositorio ha sido actualizada exitosamente.')
else:
    print(f'Error al actualizar la descripción del repositorio. Código de estado: {response.status_code}')
    print('Respuesta del servidor:', response.text)

# Archivo que interactua con las tiendas
from flask import Blueprint, render_template, request, redirect, url_for, flash  #  Importamos la librería Flask
conexion = 'prueba'

tiendas = Blueprint('tiendas', __name__, template_folder='templates')  # Creamos un objeto blueprint indicando su nombre, ruta y la carpeta con la cuál interactua

basedatos = conexion()  # Creamos una variable para almacenas los datos que regresa la función


# Parte del código para editar tiendas
@tiendas.route('/indextienda')  # Indicamos la ruta para acceder a la función indextienda
def indextienda():  # Creamos una función llamada indextienda
    try:  # Le decimos que intente el siguiente bloque de código
        cursor = basedatos.cursor()  # Creamos un objeto para interactuar y saber la conexión de la base de datos
        cursor.execute("SELECT * FROM TIENDAS")  # Ejecutamos una consulta SQL para seleccionar todos los datos de la tabla tiendas
        tiendas = cursor.fetchall()  # Almacenamos los datos de la consulta anterior
        return render_template('indextiendas.html', tiendas=tiendas)  # Renderizamos la plantilla indextiendas junto a los datos obtenidos
    except Exception as e:  # Capturamos cualquier excepción
        flash("Ocurrió un error al cargar los datos ", e)  # Mostramos un mensaje entre vistas con el error en cuestión
        tiendas = []  # Creamos una lista vacía
        return render_template('indextiendas.html', tiendas = tiendas)  # REnderizamos la plantilla indextiendas y mostramos la lista vacía

# Ruta para buscar una tienda
@tiendas.route('/buscarTienda', methods = ['GET', 'POST'])  # Indicamos la ruta para acceder a la función buscarTienda e indicamos los métodos
def buscarTienda():  # Definimos la función buscar tiendas
    try:  # Intentamos el siguiente bloque de código
        if request.method == 'POST':  # Verificamos el método 
            nombreti = request.form['nombreti']  # Obtenemos el nombre de la tienda
            cursor = basedatos.cursor()  # Creamos un objeto para saber la conexión e interactuar con la base de datos
            cursor.execute("SELECT * FROM TIENDAS")  # Ejecutamos una consulta SQL
            tiendas = cursor.fetchall()  # Guardamos los datos arrojados de la consulta
            cursor.execute("SELECT * FROM TIENDAS WHERE NOMBRE = %s", (nombreti))  # Buscamos en la tabla tiendas específicamente por nombre
            tiendas_buscadas = cursor.fetchall()  # Guardamos los datos arrojados de esa busqueda
            if tiendas_buscadas:  # Se verifica que hay datos en la variable
                flash("Tienda encontrada")  # Enviamos un mensaje entre vistas confirmando
                return render_template('indextiendas.html', tiendas = tiendas, tiendas_buscadas = tiendas_buscadas)  # Renderizamos la plantilla indextiendas junto a las tiendas y la tienda específica
            else:  # Si no hubo ninguna tienda
                flash("Tienda no encontrada")  # Envía un mensaje entre vistas diciendo que no la encontró
        return render_template('indextiendas.html', tiendas = tiendas)  # Renderiza la plantilla y muestra los datos de la tabla
    except Exception as e:  # Si ocurre alguna excepción
        flash("Ocurrió un error al buscar la tiendas ", e)  # Envía un mensaje entre vistas mostrando el error
        tiendas = []  # Inicializa una lista vacía
        return render_template('indextiendas.html', tiendas = tiendas)  # Renderiza la plantilla indextiendas junto a los datos de la tabla

# Ruta para ingresar una tienda
@tiendas.route('/agregar_tiendas', methods = ['POST'])  # Indicamos la ruta para acceder a la función ingresarTienda y especificamos el método
def ingresarTienda():  # Definimos una función llamda ingresarTienda
    # Creamos una nueva tienda en la base de datos
    try:  # Intentamos el siguiente bloque de código
        if request.method == 'POST':  # Verificamos el método del formulario
            nombreti = request.form['nombreti']  # Obtenemos el nombre de la tienda
            ubicacionti = request.form['ubicacionti']  # Obtenemos la ubicación de la tienda
            direccionti = request.form['direccionti']  # Obtenemos la dirección de la tienda
            cursor = basedatos.cursor()  # Creamos un objeto para saber la conexión y poder interactuar con la base de datos
            cursor.execute("INSERT INTO TIENDAS (NOMBRE, UBICACION, DIRECCION) VALUE (%s, %s, %s)", (nombreti, ubicacionti, direccionti))  # Ejecutamos una consulta SQL para ingresar datos dentro de la tabla TIENDAS
            basedatos.commit()  # Guardamos los cambios realizados en la base de datos
            flash('Nueva tienda ingresada con exito')  # Enviamos un mensaje entre ventanas confirmando la acción 
            return redirect(url_for('tiendas.indextienda'))  # Nos redirige a la página de indextienda
    except Exception as e:  # Si ocurre alguna excepción
        flash("Ocurrió un error al ingresar la tienda ", e)  # Manda un mensaje entre ventanas con el error
        return redirect(url_for('tiendas.indextienda'))  # Nos redirige a la página de indextienda

# Ruta para la ventana de editar tiendas
@tiendas.route('/editarTienda/<id>')  # Específicamos la ruta, y el parametro para la siguiente función
def obtenerTienda(id):  # Definimos la función obtenerTienda con el id como parámetro
    try:  # Intentamos el siguiente bloque de código
        cursor = basedatos.cursor()  # Creamos un objeto para saber la conexión de la base de datos y poder interactuar con ella
        cursor.execute("SELECT * FROM TIENDAS WHERE ID = %s", (id))  # Buscamos una tienda específica mediante el ID
        datos = cursor.fetchall()  # Guardamos los resultados de la búsqueda anterior
        return render_template('editartienda.html', datos=datos[0])  # Renderizamos la plantilla editartienda junto a los datos obtenidos
    except Exception as e:  # Si ocurre alguna excepción
        flash("Ocurrió un error al obtener la tiendas ", e)  # Manda un mensaje entre ventanas junto al error
        return render_template('editartienda.html')  # Renderizamos la plantilla de editartiendas

# Ruta para actualizar tienda
@tiendas.route('/actualizarTienda/<id>', methods = ['POST'])  # Indicamos la ruta, junto al parámetro y método
def actualizarTienda(id):  # Creamos una función llamda actualizarTienda junto al id como parámetro
    try:  # Intentamos el siguiente bloque de código
        if request.method == 'POST':  # Verificamos el método del formulario
            nombreti = request.form['nombreti']  # Obtenemos el nombre de la tienda
            ubicacionti = request.form['ubicacionti']  # Obtenemos la ubicación de la tienda
            direccionti = request.form['direccionti']  # Obtenemos la dirección de la tienda
            cursor = basedatos.cursor()  # Creamos un objeto para saber la conexión y poder interactuar con la base de datos
            cursor.execute("UPDATE TIENDAS SET NOMBRE = %s, UBICACION = %s, DIRECCION = %s WHERE ID = %s", (nombreti, ubicacionti, direccionti, id))  # Ejecutamos una consulta SQL para poder actualizar los datos de la tabla TIENDAS
            basedatos.commit()  # Guardamos los cambios hechos en la base de datos
            flash("La tienda se modificó correctamente")  # Mandamos un mensaje entre ventanas confirmando la acción
            return redirect(url_for('tiendas.indextienda'))  # Nos redirecciona al indextienda
    except Exception as e:  # Captura cualquier excepción en la variable e
        flash("Ocurrió un error al actualizar la tienda ", e)  # Manda un mensaje entre ventanas junto al error
        return redirect(url_for('tiendas.indextienda'))  # Nos redirecciona al indextienda

# Ruta para eliminar tiendas
@tiendas.route('/eliminarTienda/<string:id>', methods=['GET', 'POST']) # Se define la ruta para acceder a la función eliminarTienda y los métodos permitidos.
def eliminarTienda(id):#Define una función en un programa de Python llamada "eliminarTienda".
    try: #La palabra clave "try" se utiliza en Python para manejar excepciones.
        cursor = basedatos.cursor() # Se establece la conexión a la base de datos.
        cursor.execute("SELECT * FROM TIENDAS WHERE ID = {0}".format(id)) # Se ejecuta la consulta para obtener la tienda a eliminar.
        tienda = cursor.fetchone() # Se obtiene la tienda a eliminar.
        if not tienda: # Si la tienda no existe, se muestra un mensaje de error y se redirige a la página principal.
            flash('El producto no existe') #es un método en la biblioteca Flask de Python que se utiliza para enviar mensajes temporales entre las solicitudes.
            return redirect(url_for('tiendas.index')) #son métodos de la biblioteca Flask de Python que se utilizan para redirigir al usuario a una nueva ubicación en la aplicación web.
        if request.method == 'POST': # Si se envió un formulario de tipo POST, se elimina la tienda de la base de datos.
            cursor.execute("DELETE FROM TIENDAS WHERE ID = {0}".format(id)) # Se ejecuta la consulta para eliminar la tienda.
            basedatos.commit() # Se guarda la transacción en la base de datos.
            flash('Tienda removido correctamente') # Se muestra un mensaje de éxito.
            return redirect(url_for('tiendas.indextienda')) # Se redirige a la página principal.
        return render_template('eliminarTienda.html', tienda=tienda) # Se muestra la página para confirmar la eliminación de la tienda.
    except Exception as e: # Si ocurre algún error, se muestra un mensaje de error y se redirige a la página principal.
        flash("Ocurrió un error al eliminar la tienda ", e)#es un método en la biblioteca Flask de Python que se utiliza para enviar mensajes temporales entre las solicitudes.
        return redirect(url_for('tiendas.indextienda'))#son métodos de la biblioteca Flask de Python que se utilizan para redirigir al usuario a una nueva ubicación en la aplicación web.
