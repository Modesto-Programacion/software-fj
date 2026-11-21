"""
Software FJ - Clase Cliente
Curso: Programación (213023) - UNAD - Fase 4
Archivo: cliente.py

Cliente hereda de Entidad. Guarda los datos personales de forma
encapsulada (atributos privados) y valida cada dato antes de aceptarlo.
Cuando un dato es inválido se lanza ErrorCliente con un mensaje claro.
"""

from entidad import Entidad
from excepciones import ErrorCliente
from registro import registrar_evento


class Cliente(Entidad):
    """Cliente de Software FJ con validaciones estrictas."""

    def __init__(self, nombre, documento, correo, telefono):
        # Primero se validan todos los datos (si alguno falla, se lanza error)
        nombre = self.__validar_nombre(nombre)
        documento = self.__validar_documento(documento)
        correo = self.__validar_correo(correo)
        telefono = self.__validar_telefono(telefono)

        # Se llama al constructor del padre: el documento es el identificador
        super().__init__(documento)

        # ENCAPSULACIÓN: los datos personales son privados
        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

        # Se registra el evento en el log solo si el cliente fue válido
        registrar_evento(f"Cliente creado: {self.__nombre} ({self.__documento})")

    # ------------------------------------------------------------------
    # Propiedades de solo lectura (getters)
    # ------------------------------------------------------------------
    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    # ------------------------------------------------------------------
    # Método abstracto del padre, ahora implementado (POLIMORFISMO)
    # ------------------------------------------------------------------
    def describir(self):
        return (f"Cliente: {self.__nombre} | Documento: {self.__documento} | "
                f"Correo: {self.__correo} | Teléfono: {self.__telefono}")

    # ------------------------------------------------------------------
    # Validaciones (métodos privados de la clase)
    # ------------------------------------------------------------------
    @staticmethod
    def __validar_nombre(nombre):
        """El nombre no puede ser vacío y solo lleva letras y espacios."""
        if nombre is None or not str(nombre).strip():
            raise ErrorCliente("El nombre es obligatorio")
        nombre = str(nombre).strip()
        if len(nombre) < 3:
            raise ErrorCliente("El nombre debe tener al menos 3 caracteres")
        # Se revisa letra por letra que sea una letra o un espacio
        if not all(letra.isalpha() or letra.isspace() for letra in nombre):
            raise ErrorCliente("El nombre solo puede tener letras y espacios")
        return nombre

    @staticmethod
    def __validar_documento(documento):
        """El documento debe tener solo dígitos, entre 6 y 12."""
        if documento is None or not str(documento).strip():
            raise ErrorCliente("El documento es obligatorio")
        documento = str(documento).strip()
        try:
            # Se intenta convertir a número para comprobar que son solo dígitos
            int(documento)
        except ValueError as error:
            # ENCADENAMIENTO DE EXCEPCIONES: se conserva el error original
            raise ErrorCliente("El documento debe contener solo números") from error
        if not documento.isdigit() or not 6 <= len(documento) <= 12:
            raise ErrorCliente("El documento debe tener entre 6 y 12 dígitos")
        return documento

    @staticmethod
    def __validar_correo(correo):
        """El correo debe tener un solo @ y un punto después del @."""
        if correo is None or not str(correo).strip():
            raise ErrorCliente("El correo es obligatorio")
        correo = str(correo).strip()
        partes = correo.split("@")
        if " " in correo or len(partes) != 2 or not partes[0] or "." not in partes[1]:
            raise ErrorCliente("El correo no tiene un formato válido")
        # Después del último punto debe haber texto (por ejemplo, .com)
        if partes[1].startswith(".") or partes[1].endswith("."):
            raise ErrorCliente("El correo no tiene un formato válido")
        return correo

    @staticmethod
    def __validar_telefono(telefono):
        """El teléfono debe tener exactamente 10 dígitos."""
        if telefono is None or not str(telefono).strip():
            raise ErrorCliente("El teléfono es obligatorio")
        telefono = str(telefono).strip()
        try:
            int(telefono)
        except ValueError as error:
            # ENCADENAMIENTO DE EXCEPCIONES
            raise ErrorCliente("El teléfono debe contener solo números") from error
        if not telefono.isdigit() or len(telefono) != 10:
            raise ErrorCliente("El teléfono debe tener 10 dígitos")
        return telefono
