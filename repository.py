import os
import sqlite3
from datetime import datetime


class Repository:
    def __init__(self, db_path="db/control_camiones.db"):
        self.db_path = db_path
        self._ensure_db_folder()
        self._initialize_db()

    # -----------------------------
    # Configuración de la base de datos
    # -----------------------------
    def _ensure_db_folder(self):
        folder = os.path.dirname(self.db_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_db(self):
        # Crear tablas si no existen
        conn = self._connect()
        cursor = conn.cursor()

        # Tabla de registros de camiones
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS registros_camiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT NOT NULL,
                empresa TEXT,
                hora_entrada TEXT NOT NULL,
                hora_salida TEXT
            )
        """
        )

        # Tabla de referencia para autocompletar empresa
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS camiones_ref (
                matricula TEXT PRIMARY KEY,
                empresa TEXT
            )
        """
        )

        conn.commit()
        conn.close()

    # -----------------------------
    # CRUD de registros de camiones
    # -----------------------------
    def listar_camiones(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registros_camiones ORDER BY hora_entrada ASC")
        filas = cursor.fetchall()
        conn.close()

        resultado = []
        for fila in filas:
            estado = "Dentro" if fila["hora_salida"] is None else "Fuera"
            resultado.append(
                {
                    "id": fila["id"],
                    "matricula": fila["matricula"],
                    "empresa": fila["empresa"],
                    "entrada": fila["hora_entrada"],
                    "salida": fila["hora_salida"],
                    "estado": estado,
                }
            )
        return resultado

    def registrar_entrada(self, matricula, empresa=""):
        if not matricula:
            raise ValueError("La matrícula es obligatoria")

        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO registros_camiones (matricula, empresa, hora_entrada, hora_salida)
            VALUES (?, ?, ?, NULL)
        """,
            (matricula, empresa, ahora),
        )
        conn.commit()
        conn.close()

    def registrar_salida(self, registro_id):
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hora_salida FROM registros_camiones WHERE id=?", (registro_id,)
        )
        fila = cursor.fetchone()
        if fila is None:
            conn.close()
            raise ValueError("Registro no encontrado")
        if fila["hora_salida"] is not None:
            conn.close()
            raise ValueError("Este camión ya tiene salida registrada")
        cursor.execute(
            "UPDATE registros_camiones SET hora_salida=? WHERE id=?",
            (ahora, registro_id),
        )
        conn.commit()
        conn.close()

    def editar_registro(self, registro_id, matricula, empresa):
        if not matricula:
            raise ValueError("La matrícula no puede estar vacía")
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE registros_camiones SET matricula=?, empresa=? WHERE id=?",
            (matricula, empresa, registro_id),
        )
        conn.commit()
        conn.close()

    # -----------------------------
    # CRUD de camiones_ref (autocompletar empresa)
    # -----------------------------
    def get_empresa_by_matricula(self, matricula):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT empresa FROM camiones_ref WHERE matricula=?", (matricula,)
        )
        fila = cursor.fetchone()
        conn.close()
        if fila:
            return fila["empresa"]
        return None

    def add_or_update_camion_ref(self, matricula, empresa):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO camiones_ref (matricula, empresa)
            VALUES (?, ?)
            ON CONFLICT(matricula) DO UPDATE SET empresa=excluded.empresa
        """,
            (matricula, empresa),
        )
        conn.commit()
        conn.close()

    # -----------------------------
    # Obtener registro activo por matrícula
    # -----------------------------
    def get_registro_activo_por_matricula(self, matricula):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM registros_camiones WHERE matricula=? AND hora_salida IS NULL",
            (matricula,),
        )
        fila = cursor.fetchone()
        conn.close()

        if fila:
            return {
                "id": fila["id"],
                "matricula": fila["matricula"],
                "empresa": fila["empresa"],
                "entrada": fila["hora_entrada"],
                "salida": fila["hora_salida"],
                "estado": "Dentro",
            }
        return None
