import sqlite3
from pathlib import Path

DB_PATH = Path("db/control_camiones.db")

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_tables():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            empresa TEXT NOT NULL,
            camionero TEXT NOT NULL,
            observaciones TEXT,
            fecha_hora TEXT NOT NULL
        );
        """)
