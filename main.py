from database import create_tables
from repository import insertar_registro

def mostrar_menu():
    print("\n--- CONTROL DE CAMIONES ---")
    print("1. Registrar camión")
    print("2. Salir")

def registrar_camion():
    matricula = input("Matrícula: ").strip().upper()
    empresa = input("Empresa: ").strip()
    camionero = input("Camionero: ").strip()
    observaciones = input("Observaciones (opcional): ").strip()

    insertar_registro(matricula, empresa, camionero, observaciones)
    print("✅ Registro guardado correctamente")

def main():
    create_tables()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_camion()
        elif opcion == "2":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    main()
