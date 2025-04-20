from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://localhost:5001"

@app.route('/')
def index():
    response = requests.get(f"{API_URL}/books")
    libros = response.json() if response.ok else []
    return render_template('index.html', libros=libros)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nuevo_libro = {
            "titulo": request.form['titulo'],
            "autor": request.form['autor'],
            "genero": request.form['genero'],
            "estado": request.form['estado'].lower()
        }
        requests.post(f"{API_URL}/books", json=nuevo_libro)
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<libro_id>', methods=['GET', 'POST'])
def editar(libro_id):
    if request.method == 'POST':
        datos = {
            "titulo": request.form['titulo'],
            "autor": request.form['autor'],
            "genero": request.form['genero'],
            "estado": request.form['estado'].lower()
        }
        requests.put(f"{API_URL}/books/{libro_id}", json=datos)
        return redirect(url_for('index'))
    libro = requests.get(f"{API_URL}/books/{libro_id}").json()
    return render_template('editar.html', libro=libro)

@app.route('/eliminar/<libro_id>', methods=['GET', 'POST'])
def eliminar(libro_id):
    if request.method == 'POST':
        requests.delete(f"{API_URL}/books/{libro_id}")
        return redirect(url_for('index'))
    libro = requests.get(f"{API_URL}/books/{libro_id}").json()
    return render_template('eliminar.html', libro=libro)

if __name__ == '__main__':
    app.run(debug=True)
