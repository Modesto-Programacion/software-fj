"""
Software FJ - Registro de eventos y errores (logs)
Curso: Programación (213023) - UNAD - Fase 4
Archivo: registro.py

Escribe en el archivo logs/sistema.log. Es el único uso de archivos
permitido en el proyecto (no hay base de datos).
"""

import logging
import os

# Carpeta "logs" junto a este archivo (así funciona en cualquier computador)
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
RUTA_LOG = os.path.join(CARPETA_LOGS, "sistema.log")

# Si la carpeta no existe, se crea automáticamente
os.makedirs(CARPETA_LOGS, exist_ok=True)

# Se configura el logger: nombre del archivo, formato y codificación
_logger = logging.getLogger("software_fj")
_logger.setLevel(logging.INFO)

# Se evita agregar el manejador dos veces si el módulo se importa de nuevo
if not _logger.handlers:
    _manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    _manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    _logger.addHandler(_manejador)


def registrar_evento(mensaje):
    """Guarda un evento informativo (por ejemplo, 'Cliente registrado')."""
    _logger.info(mensaje)


def registrar_error(error):
    """Guarda un error con el nombre de su clase y su mensaje.

    Si el error fue encadenado (raise ... from ...), también se registra
    la causa original.
    """
    texto = f"{type(error).__name__}: {error}"
    # __cause__ contiene el error original cuando se usa "raise ... from ..."
    if error.__cause__ is not None:
        texto += f" | Causa: {type(error.__cause__).__name__}: {error.__cause__}"
    _logger.error(texto)
