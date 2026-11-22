"""
Software FJ - Reservas
Curso: Programación (213023) - UNAD - Fase 4
Archivo: reserva.py

La clase Reserva integra un cliente, un servicio, una duración (horas)
y un estado. Permite confirmar, cancelar y procesar la reserva, y en cada
operación usa excepciones para evitar acciones no permitidas.

Estados posibles de una reserva:
    pendiente -> confirmada -> procesada
    pendiente / confirmada -> cancelada
"""

from entidad import Entidad
from cliente import Cliente
from servicio import Servicio
from excepciones import (ErrorSistema, ErrorReserva, ErrorServicioNoDisponible,
                         ErrorValidacion)
from registro import registrar_evento, registrar_error


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    # Estados permitidos (constantes de la clase)
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    PROCESADA = "procesada"
    CANCELADA = "cancelada"

    # Contador para dar un identificador único a cada reserva
    _contador = 0

    def __init__(self, cliente, servicio, horas):
        # --- Validaciones: si algo falla se lanza ErrorReserva ---
        if cliente is None:
            raise ErrorReserva("Falta el cliente de la reserva")
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("El cliente de la reserva no es válido")
        if servicio is None:
            raise ErrorReserva("Falta el servicio de la reserva")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("El servicio de la reserva no es válido")
        if not servicio.disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{servicio.nombre}' no está disponible"
            )

        try:
            # El propio servicio valida las horas con sus reglas
            servicio.validar_parametros(horas)
        except ErrorValidacion as error:
            # ENCADENAMIENTO DE EXCEPCIONES: se conserva el error original
            raise ErrorReserva(f"Duración inválida: {error}") from error

        # Se genera el identificador (RES-001, RES-002, ...)
        Reserva._contador += 1
        super().__init__(f"RES-{Reserva._contador:03d}")

        # ENCAPSULACIÓN: atributos privados
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        self.__estado = self.PENDIENTE
        self.__costo_total = None

        registrar_evento(
            f"Reserva {self.id} creada: {cliente.nombre} -> "
            f"{servicio.nombre} ({horas} h)"
        )

    # ------------------------------------------------------------------
    # Propiedades de solo lectura
    # ------------------------------------------------------------------
    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def horas(self):
        return self.__horas

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    # ------------------------------------------------------------------
    # Acciones sobre la reserva
    # ------------------------------------------------------------------
    def confirmar(self):
        """Confirma la reserva. Solo se puede si está pendiente."""
        if self.__estado == self.CANCELADA:
            raise ErrorReserva(f"La reserva {self.id} está cancelada y no se puede confirmar")
        if self.__estado == self.PROCESADA:
            raise ErrorReserva(f"La reserva {self.id} ya fue procesada")
        if self.__estado == self.CONFIRMADA:
            raise ErrorReserva(f"La reserva {self.id} ya está confirmada")
        # Antes de confirmar, el servicio debe seguir disponible
        if not self.__servicio.disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{self.__servicio.nombre}' ya no está disponible"
            )
        self.__estado = self.CONFIRMADA
        registrar_evento(f"Reserva {self.id} confirmada")
        return self.__estado

    def cancelar(self):
        """Cancela la reserva. No se puede cancelar una ya procesada o cancelada."""
        if self.__estado == self.CANCELADA:
            raise ErrorReserva(f"La reserva {self.id} ya estaba cancelada")
        if self.__estado == self.PROCESADA:
            raise ErrorReserva(f"La reserva {self.id} ya fue procesada y no se puede cancelar")
        self.__estado = self.CANCELADA
        registrar_evento(f"Reserva {self.id} cancelada")
        return self.__estado

    # SOBRECARGA mediante parámetros opcionales:
    #   procesar()                    -> impuesto 19 % y sin descuento
    #   procesar(0.10)                -> impuesto propio
    #   procesar(0.19, 0.05)          -> impuesto y descuento
    def procesar(self, impuesto=0.19, descuento=0.0):
        """Calcula el costo y deja la reserva como procesada.

        Solo se puede procesar una reserva confirmada. Devuelve el costo total.
        """
        if self.__estado != self.CONFIRMADA:
            raise ErrorReserva(
                f"La reserva {self.id} debe estar confirmada para procesarse "
                f"(estado actual: {self.__estado})"
            )
        try:
            # try: se intenta calcular el costo con el servicio
            costo = self.__servicio.calcular_costo(self.__horas, impuesto, descuento)
        except ErrorSistema as error:
            # except: se registra el error y se relanza como ErrorReserva
            registrar_error(error)
            raise ErrorReserva(f"No se pudo procesar la reserva {self.id}") from error
        else:
            # else: solo se ejecuta si el cálculo salió bien
            self.__costo_total = costo
            self.__estado = self.PROCESADA
            registrar_evento(f"Reserva {self.id} procesada. Total: ${costo:,.2f}")
            return costo
        finally:
            # finally: se ejecuta siempre, haya o no error
            registrar_evento(f"Fin del intento de procesar la reserva {self.id}")

    # ------------------------------------------------------------------
    # Método abstracto del padre, ahora implementado (POLIMORFISMO)
    # ------------------------------------------------------------------
    def describir(self):
        texto = (f"Reserva {self.id} | Cliente: {self.__cliente.nombre} | "
                 f"Servicio: {self.__servicio.nombre} | Horas: {self.__horas} | "
                 f"Estado: {self.__estado}")
        if self.__costo_total is not None:
            texto += f" | Total: ${self.__costo_total:,.2f}"
        return texto
