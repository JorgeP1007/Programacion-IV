from flask import Flask, render_template, request, redirect, url_for
import redis
import json
import uuid

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.route('/')
def index():
    libros = []
    for key in r.scan_iter("libro:*"):
        libros.append(json.loads(r.get(key)))
    return render_template('index.html', libros=libros)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        libro_id = str(uuid.uuid4())
        libro = {
            "id": libro_id,
            "titulo": request.form['titulo'],
            "autor": request.form['autor'],
            "genero": request.form['genero'],
            "estado": request.form['estado'].lower()
        }
        r.set(f"libro:{libro_id}", json.dumps(libro))
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<libro_id>', methods=['GET', 'POST'])
def editar(libro_id):
    key = f"libro:{libro_id}"
    libro = json.loads(r.get(key))
    if request.method == 'POST':
        libro['titulo'] = request.form['titulo']
        libro['autor'] = request.form['autor']
        libro['genero'] = request.form['genero']
        libro['estado'] = request.form['estado'].lower()
        r.set(key, json.dumps(libro))
        return redirect(url_for('index'))
    return render_template('editar.html', libro=libro)

@app.route('/eliminar/<libro_id>')
def eliminar(libro_id):
    r.delete(f"libro:{libro_id}")
    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET'])
def buscar():
    criterio = request.args.get('criterio')
    valor = request.args.get('valor', '').lower()
    resultados = []
    for key in r.scan_iter("libro:*"):
        libro = json.loads(r.get(key))
        if valor in libro.get(criterio, '').lower():
            resultados.append(libro)
    return render_template('index.html', libros=resultados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

