import pymysql
from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.orm import sessionmaker, declarative_base

# Asegurar que pymysql está registrado como driver de MySQL
pymysql.install_as_MySQLdb()

# Configuración de la base de datos MariaDB
DATABASE_URL = "mysql+pymysql://usuario:password@127.0.0.1:3306/biblioteca"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Definir el modelo de datos
class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    genero = Column(String(100), nullable=False)
    estado_lectura = Column(Enum("Leído", "No leído"), nullable=False)

# Crear la tabla en la base de datos
try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
    exit(1)

def agregar_libro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura (Leído/No leído): ")
    if estado not in ["Leído", "No leído"]:
        print("Estado inválido. Debe ser 'Leído' o 'No leído'.")
        return
    nuevo_libro = Libro(titulo=titulo, autor=autor, genero=genero, estado_lectura=estado)
    session.add(nuevo_libro)
    session.commit()
    print("Libro agregado exitosamente.")

def actualizar_libro():
    id_libro = input("ID del libro a actualizar: ")
    libro = session.query(Libro).filter_by(id=id_libro).first()
    if not libro:
        print("Libro no encontrado.")
        return
    libro.titulo = input(f"Nuevo título ({libro.titulo}): ") or libro.titulo
    libro.autor = input(f"Nuevo autor ({libro.autor}): ") or libro.autor
    libro.genero = input(f"Nuevo género ({libro.genero}): ") or libro.genero
    libro.estado_lectura = input(f"Nuevo estado de lectura ({libro.estado_lectura}): ") or libro.estado_lectura
    session.commit()
    print("Libro actualizado exitosamente.")

def eliminar_libro():
    id_libro = input("ID del libro a eliminar: ")
    libro = session.query(Libro).filter_by(id=id_libro).first()
    if libro:
        session.delete(libro)
        session.commit()
        print("Libro eliminado exitosamente.")
    else:
        print("Libro no encontrado.")

def ver_libros():
    libros = session.query(Libro).all()
    if not libros:
        print("No hay libros en la biblioteca.")
    else:
        for libro in libros:
            print(f"ID: {libro.id} | Título: {libro.titulo} | Autor: {libro.autor} | Género: {libro.genero} | Estado: {libro.estado_lectura}")

def buscar_libros():
    criterio = input("Buscar por (título/autor/género): ").lower()
    if criterio not in ["título", "autor", "género"]:
        print("Criterio inválido.")
        return
    valor = input(f"Ingrese el {criterio} a buscar: ")
    columna = "titulo" if criterio == "título" else criterio
    libros = session.query(Libro).filter(getattr(Libro, columna).ilike(f"%{valor}%")).all()
    if not libros:
        print("No se encontraron libros.")
    else:
        for libro in libros:
            print(f"ID: {libro.id} | Título: {libro.titulo} | Autor: {libro.autor} | Género: {libro.genero} | Estado: {libro.estado_lectura}")

def menu():
    while True:
        print("\n--- Biblioteca Personal ---")
        print("1. Agregar libro")
        print("2. Actualizar libro")
        print("3. Eliminar libro")
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
            print("Saliendo del programa.")
            session.close()
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
