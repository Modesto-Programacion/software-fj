"""
Software FJ - Clase abstracta Entidad
Curso: Programación (213023) - UNAD - Fase 4
Archivo: entidad.py

Entidad representa cualquier objeto general del sistema que tenga un
identificador. Es una clase ABSTRACTA: no se puede crear directamente,
solo a través de clases hijas (por ejemplo, Cliente) que implementen
el método describir().
"""

from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta base para las entidades del sistema."""

    def __init__(self, identificador):
        # ENCAPSULACIÓN: el identificador es privado (doble guion bajo)
        self.__id = identificador

    @property
    def id(self):
        """Permite leer el identificador, pero no modificarlo desde afuera."""
        return self.__id

    @abstractmethod
    def describir(self):
        """Método abstracto: cada clase hija debe escribir su propia versión."""
        pass

    def __str__(self):
        # Al imprimir una entidad se muestra su descripción
        return self.describir()
