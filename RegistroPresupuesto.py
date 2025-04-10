import os

articulos = []


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresiona Enter para continuar...")


def registrar_articulo():
    limpiar_pantalla()
    nombre = input("Nombre del artículo: ").strip()
    cantidad = int(input("Cantidad: "))
    precio = float(input("Precio por unidad: $"))
    articulos.append({
        "nombre": nombre,
        "cantidad": cantidad,
        "precio": precio
    })
    print(f"\n✅ Artículo '{nombre}' registrado.")
    pausar()


def buscar_articulo():
    limpiar_pantalla()
    nombre = input("Nombre del artículo a buscar: ").strip()
    encontrados = [a for a in articulos if nombre.lower() in a['nombre'].lower()]

    if encontrados:
        print("\n📋 Artículos encontrados:")
        for i, a in enumerate(encontrados, start=1):
            print(f"{i}. {a['nombre']} - Cantidad: {a['cantidad']} - Precio: ${a['precio']}")
    else:
        print("❌ No se encontró ningún artículo con ese nombre.")
    pausar()


def editar_articulo():
    limpiar_pantalla()
    nombre = input("Nombre del artículo a editar: ").strip()
    for a in articulos:
        if a['nombre'].lower() == nombre.lower():
            print(f"\nArtículo encontrado: {a}")
            nuevo_nombre = input("Nuevo nombre (dejar en blanco para no cambiar): ").strip()
            nueva_cantidad = input("Nueva cantidad (dejar en blanco para no cambiar): ").strip()
            nuevo_precio = input("Nuevo precio (dejar en blanco para no cambiar): ").strip()

            if nuevo_nombre:
                a['nombre'] = nuevo_nombre
            if nueva_cantidad:
                a['cantidad'] = int(nueva_cantidad)
            if nuevo_precio:
                a['precio'] = float(nuevo_precio)

            print("\n✅ Artículo actualizado.")
            break
    else:
        print("❌ Artículo no encontrado.")
    pausar()


def eliminar_articulo():
    limpiar_pantalla()
    nombre = input("Nombre del artículo a eliminar: ").strip()
    for a in articulos:
        if a['nombre'].lower() == nombre.lower():
            articulos.remove(a)
            print(f"\n✅ Artículo '{nombre}' eliminado.")
            break
    else:
        print("❌ Artículo no encontrado.")
    pausar()


def ver_presupuesto():
    limpiar_pantalla()
    if not articulos:
        print("No hay artículos registrados.")
    else:
        total = 0
        print("📦 Lista de artículos:")
        for i, a in enumerate(articulos, start=1):
            subtotal = a['cantidad'] * a['precio']
            total += subtotal
            print(
                f"{i}. {a['nombre']} - Cantidad: {a['cantidad']} - Precio: ${a['precio']} - Subtotal: ${subtotal:.2f}")
        print(f"\n💰 Total del presupuesto: ${total:.2f}")
    pausar()


def menu():
    while True:
        limpiar_pantalla()
        print("📝 Sistema de Registro de Presupuesto")
        print("1. Registrar artículo")
        print("2. Buscar artículo")
        print("3. Editar artículo")
        print("4. Eliminar artículo")
        print("5. Ver presupuesto")
        print("6. Salir")

        opcion = input("\nSelecciona una opción: ")
        if opcion == "1":
            registrar_articulo()
        elif opcion == "2":
            buscar_articulo()
        elif opcion == "3":
            editar_articulo()
        elif opcion == "4":
            eliminar_articulo()
        elif opcion == "5":
            ver_presupuesto()
        elif opcion == "6":
            print("\n👋 ¡Hasta luego!")
            break
        else:
            print("⚠️ Opción inválida.")
            pausar()


if __name__ == "__main__":
    menu()


