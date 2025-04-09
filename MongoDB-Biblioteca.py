import pymongo
from pymongo import MongoClient
import sys

# Conexión a MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client["biblioteca"]
coleccion_libros = db["libros"]


def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura (leído/no leído): ").lower()
    libro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }
    coleccion_libros.insert_one(libro)
    print("Libro agregado exitosamente.\n")

def actualizar_libro():
    titulo = input("Ingrese el título del libro a actualizar: ")
    libro = coleccion_libros.find_one({"titulo": titulo})
    if libro:
        print("Libro encontrado. ¿Qué deseas actualizar?")
        campo = input("Campo a actualizar (titulo/autor/genero/estado): ").lower()
        nuevo_valor = input(f"Nuevo valor para {campo}: ")
        coleccion_libros.update_one({"_id": libro["_id"]}, {"$set": {campo: nuevo_valor}})
        print("Libro actualizado correctamente.\n")
    else:
        print("Libro no encontrado.\n")

def eliminar_libro():
    titulo = input("Ingrese el título del libro a eliminar: ")
    resultado = coleccion_libros.delete_one({"titulo": titulo})
    if resultado.deleted_count > 0:
        print("Libro eliminado exitosamente.\n")
    else:
        print("Libro no encontrado.\n")

def ver_libros():
    libros = coleccion_libros.find()
    print("\nListado de libros:")
    for libro in libros:
        print(f"Título: {libro['titulo']}, Autor: {libro['autor']}, Género: {libro['genero']}, Estado: {libro['estado']}")
    print("")

def buscar_libros():
    criterio = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input(f"Ingrese el valor para {criterio}: ")
    resultados = coleccion_libros.find({criterio: {"$regex": valor, "$options": "i"}})
    print("\nResultados de la búsqueda:")
    for libro in resultados:
        print(f"Título: {libro['titulo']}, Autor: {libro['autor']}, Género: {libro['genero']}, Estado: {libro['estado']}")
    print("")

def menu():
    while True:
        print("--- Biblioteca Personal ---")
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

