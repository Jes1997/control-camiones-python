from datetime import datetime
from database import get_connection


def registrar_movimiento(matricula, empresa="", camionero="", observaciones=""):
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        # Buscar si existe un registro abierto (sin hora_salida)
        cursor = conn.execute(
            """
            SELECT id FROM registros
            WHERE matricula = ? AND hora_salida IS NULL
            ORDER BY hora_entrada DESC
            LIMIT 1
        """,
            (matricula,),
        )
        registro_abierto = cursor.fetchone()

        if registro_abierto:
            # Registrar salida
            conn.execute(
                """
                UPDATE registros
                SET hora_salida = ?
                WHERE id = ?
            """,
                (hora_actual, registro_abierto[0]),
            )
            return "Salida registrada ✅"
        else:
            # Registrar entrada
            conn.execute(
                """
                INSERT INTO registros (matricula, empresa, camionero, observaciones, hora_entrada)
                VALUES (?, ?, ?, ?, ?)
            """,
                (matricula, empresa, camionero, observaciones, hora_actual),
            )
            return "Entrada registrada ✅"


def registrar_entrada(matricula, empresa, camionero, observaciones=""):
    hora_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        conn.execute(
            """
        INSERT INTO registros (matricula, empresa, camionero, observaciones, hora_entrada)
        VALUES (?, ?, ?, ?, ?)
        """,
            (matricula, empresa, camionero, observaciones, hora_entrada),
        )


def registrar_salida(matricula):
    hora_salida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        # Actualiza el registro más reciente que no tenga hora_salida
        conn.execute(
            """
        UPDATE registros
        SET hora_salida = ?
        WHERE matricula = ? AND hora_salida IS NULL
        ORDER BY hora_entrada DESC
        LIMIT 1
        """,
            (hora_salida, matricula),
        )


def listar_registros():
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM registros ORDER BY hora_entrada DESC")
        registros = cursor.fetchall()
        return registros


def obtener_registro_abierto_o_finalizado(matricula):
    """Devuelve el registro abierto o, si no hay, el último registro finalizado"""
    with get_connection() as conn:
        # Primero buscamos un registro abierto
        cursor = conn.execute(
            """
            SELECT * FROM registros
            WHERE matricula = ? AND hora_salida IS NULL
            ORDER BY hora_entrada DESC
            LIMIT 1
        """,
            (matricula,),
        )
        registro_abierto = cursor.fetchone()
        if registro_abierto:
            return registro_abierto, "abierto"

        # Si no hay abierto, devolvemos el último finalizado
        cursor = conn.execute(
            """
            SELECT * FROM registros
            WHERE matricula = ?
            ORDER BY hora_entrada DESC
            LIMIT 1
        """,
            (matricula,),
        )
        registro_finalizado = cursor.fetchone()
        if registro_finalizado:
            return registro_finalizado, "finalizado"

    return None, None


def editar_registro(
    registro_id, nuevas_observaciones=None, nueva_entrada=None, nueva_salida=None
):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE registros
            SET observaciones = COALESCE(?, observaciones),
                hora_entrada = COALESCE(?, hora_entrada),
                hora_salida = COALESCE(?, hora_salida)
            WHERE id = ?
        """,
            (nuevas_observaciones, nueva_entrada, nueva_salida, registro_id),
        )


def validar_fecha(fecha_str):
    if not fecha_str:  # vacío = no cambiar
        return True
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False


def editar_registro_menu(registro):
    while True:
        print("\n¿Qué quieres modificar?")
        print("1. Observaciones")
        print("2. Hora de entrada")
        print("3. Hora de salida")
        print("4. Cancelar")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nuevas_obs = input(f"Nuevas observaciones [{registro[4]}]: ").strip()
            editar_registro(
                registro[0], nuevas_observaciones=nuevas_obs if nuevas_obs else None
            )
            print("✅ Observaciones actualizadas")
        elif opcion == "2":
            while True:
                nueva_ent = input(f"Nueva hora de entrada [{registro[5]}]: ").strip()
                if validar_fecha(nueva_ent):
                    editar_registro(
                        registro[0], nueva_entrada=nueva_ent if nueva_ent else None
                    )
                    print("✅ Hora de entrada actualizada")
                    break
                else:
                    print("❌ Formato inválido. Usa YYYY-MM-DD HH:MM:SS")
        elif opcion == "3":
            while True:
                nueva_sal = input(f"Nueva hora de salida [{registro[6]}]: ").strip()
                if validar_fecha(nueva_sal):
                    editar_registro(
                        registro[0], nueva_salida=nueva_sal if nueva_sal else None
                    )
                    print("✅ Hora de salida actualizada")
                    break
                else:
                    print("❌ Formato inválido. Usa YYYY-MM-DD HH:MM:SS")
        elif opcion == "4":
            print("🔒 Edición cancelada")
            break
        else:
            print("❌ Opción no válida")
