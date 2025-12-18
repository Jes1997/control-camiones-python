from database import create_tables
from repository import (
    registrar_movimiento,
    listar_registros,
    obtener_registro_abierto_o_finalizado,
    editar_registro_menu,
)


def registrar_movimiento_menu():
    matricula = input("Matrícula: ").strip().upper()
    registro, estado = obtener_registro_abierto_o_finalizado(matricula)

    if estado == "finalizado":
        print("⚠️ Este registro ya tiene entrada y salida registradas:")
        print(
            f"Entrada: {registro[5]}, Salida: {registro[6]}, Observaciones: {registro[4]}"
        )
        confirmar = input("¿Quieres editar este registro? (s/n): ").strip().lower()
        if confirmar == "s":
            editar_registro_menu(registro)
        else:
            print("🔒 Registro no modificado")
    else:
        empresa = input("Empresa (solo si es entrada): ").strip()
        camionero = input("Camionero (solo si es entrada): ").strip()
        observaciones = input("Observaciones (opcional): ").strip()

        mensaje = registrar_movimiento(matricula, empresa, camionero, observaciones)
        print(mensaje)


def listar_registros_menu():
    registros = listar_registros()
    if not registros:
        print("No hay registros aún")
        return

    for r in registros:
        print(
            f"Entrada: {r[5]}, Matrícula: {r[1]}, Empresa: {r[2]}, Camionero: {r[3]}, "
            f"Salida: {r[6]}, Observaciones: {r[4]}"
        )


def main():
    create_tables()

    while True:
        print("\n--- CONTROL DE CAMIONES ---")
        print("1. Registrar movimiento (entrada/salida)")
        print("2. Listar registros")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_movimiento_menu()
        elif opcion == "2":
            listar_registros_menu()
        elif opcion == "3":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción no válida")


if __name__ == "__main__":
    main()
