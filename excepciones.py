"""
Software FJ - Excepciones personalizadas
Curso: Programación (213023) - UNAD - Fase 4
Archivo: excepciones.py

Aquí se definen los errores propios del sistema. Todas heredan de
ErrorSistema, de modo que en el código se pueda capturar cualquier error
del sistema con un solo "except ErrorSistema".
"""


class ErrorSistema(Exception):
    """Excepción base del sistema. Todas las demás heredan de esta."""

    def __init__(self, mensaje="Ocurrió un error en el sistema"):
        # Se llama al constructor de Exception para guardar el mensaje
        super().__init__(mensaje)
        # Se guarda el mensaje también como atributo para poder leerlo
        self.mensaje = mensaje


class ErrorValidacion(ErrorSistema):
    """Se lanza cuando un dato no cumple las reglas (vacío, negativo, etc.)."""

    def __init__(self, mensaje="Dato inválido"):
        super().__init__(mensaje)


class ErrorCliente(ErrorSistema):
    """Se lanza cuando los datos de un cliente son inválidos o faltan."""

    def __init__(self, mensaje="Cliente inválido"):
        super().__init__(mensaje)


class ErrorServicioNoDisponible(ErrorSistema):
    """Se lanza cuando se intenta usar un servicio que no está disponible."""

    def __init__(self, mensaje="El servicio no está disponible"):
        super().__init__(mensaje)


class ErrorReserva(ErrorSistema):
    """Se lanza cuando una reserva no se puede crear, confirmar o cancelar."""

    def __init__(self, mensaje="Operación de reserva no permitida"):
        super().__init__(mensaje)


class ErrorCalculo(ErrorSistema):
    """Se lanza cuando un cálculo de costos es inconsistente."""

    def __init__(self, mensaje="Cálculo inconsistente"):
        super().__init__(mensaje)
