from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__)

# URI = "http://localhost:8000/contactos"

URI = "https://herokubackendsql-03fb6209ab45.herokuapp.com/contactos"

# Forma en que protege la sesión
app.secret_key = 'mysecretkey'

#TODO
    # Agregar validaciones de solicitudes
    # Agregar diseño

@app.route('/')
def index():
    contactos  = requests.get(URI)
    contactos_json = json.loads(contactos.text)
    print(contactos_json)
    return render_template('index.html', contactos = contactos_json)

@app.route('/add_contact', methods=["POST"])
def add_contact():
    if request.method == "POST":
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        data = {"email":f"{email}",
        "nombre":f"{nombre}",
        "telefono":f"{telefono}"}
        requests.post(URI, json=data)
        flash('Contact Added successfully')
        return redirect(url_for('index'))

@app.route('/buscarContacto', methods=["GET","POST"])
def buscarContacto():
    if request.method == "POST":
        email = request.form['email']
        # Obtenemos el registro a buscar
        contacto_buscado  = requests.get(f"{URI}/{email}")
        contactos_buscado_json = json.loads(contacto_buscado.text)

        # Obtenemos todos los registros
        contactos = requests.get(URI)
        contactos_json = json.loads(contactos.text)
        print(contacto_buscado)
        return render_template('index.html', contactos = contactos_json, contacto_buscados = contactos_buscado_json)


@app.route('/edit/<string:email>')
def get_contact(email):
    contactos  = requests.get(f"{URI}/{email}")
    contactos_json = json.loads(contactos.text)
    return render_template('edit_contact.html', contacto = contactos_json)

@app.route('/update/<string:email>', methods=['POST'])
def update_contact(email):
    if request.method == "POST":
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        data = {"email":f"{email}",
        "nombre":f"{nombre}",
        "telefono":f"{telefono}"}
        requests.put(f"{URI}/{email}", json=data)
        flash('Contact Update successfully')
        return redirect(url_for('index'))


@app.route('/delete/<string:email>')
def delete_contact(email):
    # print(email)
    requests.delete(f'{URI}/{email}')
    flash('Se ha eliminado el registro')
    return redirect(url_for('index'))


# Solo local
# if __name__ == '__main__':
    # app.run()
    # app.run(port = 8080, debug = True)