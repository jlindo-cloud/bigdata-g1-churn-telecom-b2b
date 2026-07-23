from datetime import datetime
from typing import Optional, Dict, Any

from database import logs_collection


def save_log(
    username: str,
    endpoint: str,
    method: str,
    action: str,
    ip: Optional[str] = None,
    status_code: Optional[int] = None,
    response_time: Optional[float] = None,
    details: Optional[Dict[str, Any]] = None,
    role: Optional[str] = None
):
    """
    Guarda un registro de auditoría en MongoDB.

    Parámetros:
        username: Usuario que realizó la acción.
        endpoint: Endpoint consumido.
        method: Método HTTP (GET, POST, PUT, DELETE).
        action: Descripción de la acción.
        ip: Dirección IP del cliente.
        status_code: Código HTTP devuelto.
        response_time: Tiempo de respuesta en milisegundos.
        details: Información adicional de la petición.
        role: Rol del usuario (admin, analyst, viewer).
    """

    try:

        log = {

            "username": username,

            "role": role,

            "endpoint": endpoint,

            "method": method,

            "action": action,

            "ip": ip,

            "status_code": status_code,

            "response_time_ms": response_time,

            "details": details if details else {},

            "timestamp": datetime.utcnow()

        }

        logs_collection.insert_one(log)

    except Exception as ex:

        print(f"[AUDIT ERROR] {ex}")