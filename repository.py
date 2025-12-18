from datetime import datetime
from database import get_connection

def insertar_registro(matricula, empresa, camionero, observaciones):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        conn.execute("""
        INSERT INTO registros 
        (matricula, empresa, camionero, observaciones, fecha_hora)
        VALUES (?, ?, ?, ?, ?)
        """, (matricula, empresa, camionero, observaciones, fecha_hora))
