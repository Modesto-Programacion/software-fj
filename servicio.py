"""
Software FJ - Servicios
Curso: Programación (213023) - UNAD - Fase 4
Archivo: servicio.py

Contiene la clase ABSTRACTA Servicio y tres servicios especializados:
    - ReservaSala
    - AlquilerEquipo
    - AsesoriaEspecializada

Cada servicio hijo sobrescribe (POLIMORFISMO):
    - _costo_base()         -> cómo se calcula su costo base
    - describir()           -> cómo se describe
    - validar_parametros()  -> qué reglas propias valida

El método calcular_costo() está SOBRECARGADO con parámetros opcionales:
    calcular_costo(horas)
    calcular_costo(horas, impuesto)
    calcular_costo(horas, impuesto, descuento)
"""

from abc import abstractmethod

from entidad import Entidad
from excepciones import ErrorValidacion, ErrorCalculo
from registro import registrar_evento


def _es_numero(valor):
    """Devuelve True si el valor es un número (y no un booleano)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


class Servicio(Entidad):
    """Clase abstracta: define lo que todo servicio debe tener y hacer."""

    # Contador para dar un identificador único a cada servicio creado
    _contador = 0

    def __init__(self, nombre, tarifa_hora):
        # Se validan los datos comunes antes de crear el objeto
        nombre = self._validar_nombre(nombre)
        tarifa_hora = self._validar_tarifa(tarifa_hora)

        # Se genera el identificador (SRV-001, SRV-002, ...)
        Servicio._contador += 1
        super().__init__(f"SRV-{Servicio._contador:03d}")

        # ENCAPSULACIÓN: atributos privados
        self.__nombre = nombre
        self.__tarifa_hora = tarifa_hora
        self.__disponible = True

    # ------------------------------------------------------------------
    # Propiedades (getters y setter)
    # ------------------------------------------------------------------
    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa_hora(self):
        return self.__tarifa_hora

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        # Solo se aceptan valores True o False
        if not isinstance(valor, bool):
            raise ErrorValidacion("La disponibilidad debe ser True o False")
        self.__disponible = valor
        registrar_evento(
            f"Servicio '{self.__nombre}' marcado como "
            f"{'disponible' if valor else 'no disponible'}"
        )

    # ------------------------------------------------------------------
    # Validaciones comunes (métodos de la clase)
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_nombre(nombre):
        if nombre is None or not str(nombre).strip():
            raise ErrorValidacion("El nombre del servicio es obligatorio")
        nombre = str(nombre).strip()
        if len(nombre) < 3:
            raise ErrorValidacion("El nombre del servicio debe tener al menos 3 caracteres")
        return nombre

    @staticmethod
    def _validar_tarifa(tarifa):
        if not _es_numero(tarifa):
            raise ErrorValidacion("La tarifa por hora debe ser un número")
        if tarifa <= 0:
            raise ErrorValidacion("La tarifa por hora debe ser mayor que cero")
        return tarifa

    # Límite de horas por reserva (cada servicio hijo puede cambiarlo)
    MAX_HORAS = 24

    def validar_parametros(self, horas=None):
        """Valida los parámetros de uso del servicio (por ahora, las horas).

        Las clases hijas sobrescriben este método para agregar sus reglas.
        """
        if horas is not None:
            if not _es_numero(horas):
                raise ErrorValidacion("Las horas deben ser un número")
            if horas <= 0:
                raise ErrorValidacion("Las horas deben ser mayores que cero")
            if horas > self.MAX_HORAS:
                raise ErrorValidacion(
                    f"Este servicio no permite más de {self.MAX_HORAS} horas"
                )
        return True

    # ------------------------------------------------------------------
    # Método abstracto: cada servicio calcula su costo base de forma distinta
    # ------------------------------------------------------------------
    @abstractmethod
    def _costo_base(self, horas):
        """Costo del servicio sin impuestos ni descuentos."""
        pass

    # ------------------------------------------------------------------
    # SOBRECARGA mediante parámetros opcionales
    # ------------------------------------------------------------------
    def calcular_costo(self, horas, impuesto=0.19, descuento=0.0):
        """Calcula el costo total del servicio.

        Formas de llamarlo:
            calcular_costo(3)                 -> horas (con el impuesto por defecto)
            calcular_costo(3, 0.10)           -> horas e impuesto propio
            calcular_costo(3, 0.19, 0.10)     -> horas, impuesto y descuento
        """
        # Primero se validan las horas con las reglas de cada servicio
        self.validar_parametros(horas)

        try:
            # Se revisa que impuesto y descuento sean números razonables
            if not _es_numero(impuesto) or not _es_numero(descuento):
                raise TypeError("El impuesto y el descuento deben ser números")
            if not 0 <= impuesto <= 1:
                raise ErrorCalculo("El impuesto debe estar entre 0 y 1")
            if not 0 <= descuento <= 1:
                raise ErrorCalculo("El descuento debe estar entre 0 y 1 (0% a 100%)")

            costo = self._costo_base(horas)
            total = costo * (1 - descuento) * (1 + impuesto)
        except TypeError as error:
            # ENCADENAMIENTO DE EXCEPCIONES: se conserva el error original
            raise ErrorCalculo("No se pudo calcular el costo") from error
        else:
            # Se ejecuta solo si no hubo errores
            registrar_evento(f"Costo calculado para '{self.nombre}': ${total:,.2f}")
            return total

    def __str__(self):
        return self.describir()


# ======================================================================
# SERVICIO 1: Reserva de salas
# ======================================================================
class ReservaSala(Servicio):
    """Sala para reuniones o eventos. Las salas grandes tienen recargo."""

    MAX_HORAS = 12
    CAPACIDAD_RECARGO = 20   # a partir de esta capacidad se cobra recargo
    RECARGO_SALA_GRANDE = 0.10

    def __init__(self, nombre, tarifa_hora, capacidad):
        # Se valida la capacidad antes de crear el objeto
        if not isinstance(capacidad, int) or isinstance(capacidad, bool):
            raise ErrorValidacion("La capacidad debe ser un número entero")
        if not 1 <= capacidad <= 200:
            raise ErrorValidacion("La capacidad debe estar entre 1 y 200 personas")
        super().__init__(nombre, tarifa_hora)
        self.__capacidad = capacidad
        registrar_evento(f"Servicio creado: sala '{self.nombre}' ({capacidad} personas)")

    @property
    def capacidad(self):
        return self.__capacidad

    def _costo_base(self, horas):  # POLIMORFISMO: costo propio de la sala
        costo = self.tarifa_hora * horas
        if self.__capacidad > self.CAPACIDAD_RECARGO:
            costo *= 1 + self.RECARGO_SALA_GRANDE
        return costo

    def describir(self):  # POLIMORFISMO
        return (f"[Sala] {self.nombre} | Capacidad: {self.__capacidad} personas | "
                f"Tarifa: ${self.tarifa_hora:,.0f}/hora")

    def validar_parametros(self, horas=None):  # POLIMORFISMO
        # Reglas propias: máximo 12 horas (usa MAX_HORAS de esta clase)
        return super().validar_parametros(horas)


# ======================================================================
# SERVICIO 2: Alquiler de equipos
# ======================================================================
class AlquilerEquipo(Servicio):
    """Alquiler de equipos (proyectores, portátiles, etc.) por horas."""

    MAX_HORAS = 72

    def __init__(self, nombre, tarifa_hora, cantidad):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool):
            raise ErrorValidacion("La cantidad debe ser un número entero")
        if not 1 <= cantidad <= 50:
            raise ErrorValidacion("La cantidad debe estar entre 1 y 50 equipos")
        super().__init__(nombre, tarifa_hora)
        self.__cantidad = cantidad
        registrar_evento(f"Servicio creado: equipo '{self.nombre}' x{cantidad}")

    @property
    def cantidad(self):
        return self.__cantidad

    def _costo_base(self, horas):  # POLIMORFISMO: se cobra por cada equipo
        return self.tarifa_hora * horas * self.__cantidad

    def describir(self):  # POLIMORFISMO
        return (f"[Equipo] {self.nombre} | Cantidad: {self.__cantidad} | "
                f"Tarifa: ${self.tarifa_hora:,.0f}/hora por equipo")

    def validar_parametros(self, horas=None):  # POLIMORFISMO
        # Reglas propias: máximo 72 horas (usa MAX_HORAS de esta clase)
        return super().validar_parametros(horas)


# ======================================================================
# SERVICIO 3: Asesorías especializadas
# ======================================================================
class AsesoriaEspecializada(Servicio):
    """Asesoría de un especialista. Máximo 8 horas por sesión."""

    MAX_HORAS = 8
    RECARGO_ESPECIALISTA = 0.15

    def __init__(self, nombre, tarifa_hora, especialidad):
        if especialidad is None or len(str(especialidad).strip()) < 3:
            raise ErrorValidacion("La especialidad es obligatoria (mínimo 3 caracteres)")
        super().__init__(nombre, tarifa_hora)
        self.__especialidad = str(especialidad).strip()
        registrar_evento(f"Servicio creado: asesoría '{self.nombre}' ({self.__especialidad})")

    @property
    def especialidad(self):
        return self.__especialidad

    def _costo_base(self, horas):  # POLIMORFISMO: recargo por ser especialista
        return self.tarifa_hora * horas * (1 + self.RECARGO_ESPECIALISTA)

    def describir(self):  # POLIMORFISMO
        return (f"[Asesoría] {self.nombre} | Especialidad: {self.__especialidad} | "
                f"Tarifa: ${self.tarifa_hora:,.0f}/hora")

    def validar_parametros(self, horas=None):  # POLIMORFISMO
        # Reglas propias: máximo 8 horas (usa MAX_HORAS de esta clase)
        return super().validar_parametros(horas)
