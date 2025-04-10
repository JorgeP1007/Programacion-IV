import redis
import json
import uuid
import sys

# Conexión a KeyDB
r = redis.Redis(host='keydb', port=6379, decode_responses=True)
def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura (leído/no leído): ").lower()
    libro_id = str(uuid.uuid4())
    libro = {
        "id": libro_id,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }
    r.set(f"libro:{libro_id}", json.dumps(libro))
    print("Libro agregado exitosamente.\n")

def actualizar_libro():
    titulo = input("Ingrese el título del libro a actualizar: ")
    for key in r.scan_iter("libro:*"):
        libro = json.loads(r.get(key))
        if libro['titulo'].lower() == titulo.lower():
            campo = input("Campo a actualizar (titulo/autor/genero/estado): ").lower()
            nuevo_valor = input(f"Nuevo valor para {campo}: ")
            libro[campo] = nuevo_valor
            r.set(key, json.dumps(libro))
            print("Libro actualizado correctamente.\n")
            return
    print("Libro no encontrado.\n")

def eliminar_libro():
    titulo = input("Ingrese el título del libro a eliminar: ")
    for key in r.scan_iter("libro:*"):
        libro = json.loads(r.get(key))
        if libro['titulo'].lower() == titulo.lower():
            r.delete(key)
            print("Libro eliminado exitosamente.\n")
            return
    print("Libro no encontrado.\n")

def ver_libros():
    print("\nListado de libros:")
    for key in r.scan_iter("libro:*"):
        libro = json.loads(r.get(key))
        print(f"Título: {libro['titulo']}, Autor: {libro['autor']}, Género: {libro['genero']}, Estado: {libro['estado']}")
    print("")

def buscar_libros():
    criterio = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input(f"Ingrese el valor para {criterio}: ").lower()
    print("\nResultados de la búsqueda:")
    for key in r.scan_iter("libro:*"):
        libro = json.loads(r.get(key))
        if valor in libro[criterio].lower():
            print(f"Título: {libro['titulo']}, Autor: {libro['autor']}, Género: {libro['genero']}, Estado: {libro['estado']}")
    print("")

def menu():
    while True:
        print("--- Biblioteca Personal (KeyDB) ---")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro existente")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            actualizar_libro()
        elif opcion == "3":
            eliminar_libro()
        elif opcion == "4":
            ver_libros()
        elif opcion == "5":
            buscar_libros()
        elif opcion == "6":
            print("Saliendo del programa...")
            sys.exit()
        else:
            print("Opción no válida. Intente de nuevo.\n")

if __name__ == "__main__":
    menu()
