import sqlite3

def conectar_db():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS libros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        autor TEXT NOT NULL,
                        genero TEXT NOT NULL,
                        estado_lectura TEXT CHECK(estado_lectura IN ('Leído', 'No leído')) NOT NULL)''')
    conn.commit()
    return conn, cursor

def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura (Leído/No leído): ")
    conn, cursor = conectar_db()
    cursor.execute("INSERT INTO libros (titulo, autor, genero, estado_lectura) VALUES (?, ?, ?, ?)", (titulo, autor, genero, estado))
    conn.commit()
    conn.close()
    print("Libro agregado con éxito.\n")

def actualizar_libro():
    titulo_libro = input("Título del libro a actualizar: ")
    nuevo_estado = input("Nuevo estado de lectura (Leído/No leído): ")
    conn, cursor = conectar_db()
    cursor.execute("UPDATE libros SET estado_lectura = ? WHERE titulo = ?", (nuevo_estado, titulo_libro))
    conn.commit()
    conn.close()
    print("Libro actualizado con éxito.\n")

def eliminar_libro():
    titulo_libro = input("Título del libro a eliminar: ")
    conn, cursor = conectar_db()
    cursor.execute("DELETE FROM libros WHERE titulo = ?", (titulo_libro,))
    conn.commit()
    conn.close()
    print("Libro eliminado con éxito.\n")

def ver_libros():
    conn, cursor = conectar_db()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    conn.close()
    for libro in libros:
        print(libro)
    print("")

def buscar_libro():
    criterio = input("Buscar por (titulo, autor, genero): ").strip().lower()
    if criterio not in ["titulo", "autor", "genero"]:
        print("Criterio no válido. Intente de nuevo.\n")
        return
    valor = input(f"Ingrese {criterio}: ").strip()
    conn, cursor = conectar_db()
    cursor.execute(f"SELECT * FROM libros WHERE {criterio} LIKE ?", ('%' + valor + '%',))
    libros = cursor.fetchall()
    conn.close()
    if libros:
        for libro in libros:
            print(libro)
    else:
        print("No se encontraron libros con ese criterio.\n")

def menu():
    while True:
        print("\n--- Biblioteca Personal ---")
        print("1. Agregar libro")
        print("2. Actualizar libro")
        print("3. Eliminar libro")
        print("4. Ver listado de libros")
        print("5. Buscar libro")
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
            buscar_libro()
        elif opcion == "6":
            print("Saliendo...\n")
            break
        else:
            print("Opción no válida. Intente de nuevo.\n")

if __name__ == "__main__":
    menu()
