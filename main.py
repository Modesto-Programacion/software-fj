"""
Software FJ - Sistema integral de gestión de clientes, servicios y reservas
Curso: Programación (213023) - UNAD - Fase 4
Archivo: main.py  (simulación de operaciones)

Este archivo ejecuta más de 10 operaciones, válidas e inválidas, para
demostrar que el sistema sigue funcionando aunque ocurran errores.
Cada operación se ejecuta dentro de la función `ejecutar`, que usa
try/except/else/finally. Así, ningún error detiene el programa y todo
queda registrado en el archivo de logs (logs/sistema.log).
"""

from excepciones import ErrorSistema
from registro import registrar_evento, registrar_error
from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva

# Listas internas donde se guardan los objetos (no se usa base de datos)
clientes = []
servicios = []
reservas = []

# Contadores para el resumen final
exitosas = 0
fallidas = 0


def ejecutar(numero, descripcion, operacion):
    """Ejecuta una operación de forma segura.

    - try:     intenta ejecutar la operación.
    - except:  captura el error, lo registra y el programa continúa.
    - else:    se ejecuta solo si NO hubo error.
    - finally: se ejecuta siempre (imprime el separador).
    """
    global exitosas, fallidas
    print(f"\n[Operación {numero}] {descripcion}")
    registrar_evento(f"Operación {numero}: {descripcion}")
    try:
        resultado = operacion()
    except ErrorSistema as error:
        # Errores propios del sistema (excepciones personalizadas)
        fallidas += 1
        registrar_error(error)
        print(f"   ERROR CONTROLADO ({type(error).__name__}): {error}")
    except Exception as error:
        # Cualquier otro error inesperado: el programa tampoco se detiene
        fallidas += 1
        registrar_error(error)
        print(f"   ERROR INESPERADO ({type(error).__name__}): {error}")
    else:
        exitosas += 1
        registrar_evento(f"Operación {numero} completada correctamente")
        print(f"   OK -> {resultado}")
    finally:
        print("   " + "-" * 50)


# ---------------------------------------------------------------------------
# Definición de las operaciones (cada una es una función pequeña)
# ---------------------------------------------------------------------------
def crear_cliente(nombre, documento, correo, telefono):
    """Crea un cliente y lo guarda en la lista si es válido."""
    cliente = Cliente(nombre, documento, correo, telefono)
    clientes.append(cliente)
    return f"Cliente registrado: {cliente.nombre}"


def crear_servicio(clase, *args):
    """Crea un servicio de la clase indicada y lo guarda en la lista."""
    servicio = clase(*args)
    servicios.append(servicio)
    return servicio.describir()


def crear_reserva(cliente, servicio, horas):
    """Crea una reserva, la confirma y la procesa."""
    reserva = Reserva(cliente, servicio, horas)
    reserva.confirmar()
    costo = reserva.procesar()
    reservas.append(reserva)
    return f"Reserva procesada. Costo total: ${costo:,.2f}"


def reserva_cancelada_y_confirmada():
    """Operación no permitida: confirmar una reserva ya cancelada."""
    reserva = Reserva(clientes[0], servicios[0], 1)
    reserva.cancelar()
    reservas.append(reserva)
    reserva.confirmar()  # Debe lanzar un error controlado
    return "Esto no debería mostrarse"


def costos_sobrecargados():
    """Demuestra las tres variantes del cálculo de costo (sobrecarga)."""
    servicio = servicios[0]
    simple = servicio.calcular_costo(3)                     # solo horas
    con_impuesto = servicio.calcular_costo(3, 0.19)         # horas + impuesto
    con_descuento = servicio.calcular_costo(3, 0.19, 0.10)  # + descuento
    return (f"simple=${simple:,.2f} | con impuesto=${con_impuesto:,.2f} | "
            f"con descuento=${con_descuento:,.2f}")


def main():
    print("=" * 60)
    print("SOFTWARE FJ - Simulación de operaciones")
    print("=" * 60)
    registrar_evento("Inicio de la simulación")

    # --- Clientes (válidos e inválidos) ---
    ejecutar(1, "Registrar cliente válido (Ana)",
             lambda: crear_cliente("Ana Pérez", "1100223344",
                                   "ana@correo.com", "3001234567"))
    ejecutar(2, "Registrar cliente con correo inválido",
             lambda: crear_cliente("Luis Gómez", "1100556677",
                                   "luis-sin-arroba", "3009876543"))
    ejecutar(3, "Registrar cliente con documento vacío",
             lambda: crear_cliente("Marta Ruiz", "",
                                   "marta@correo.com", "3012223344"))
    ejecutar(4, "Registrar cliente válido (Carlos)",
             lambda: crear_cliente("Carlos Díaz", "1100889900",
                                   "carlos@correo.com", "3104445566"))

    # --- Servicios (válidos e inválidos) ---
    ejecutar(5, "Crear servicio: reserva de sala (válido)",
             lambda: crear_servicio(ReservaSala, "Sala Ejecutiva", 50000, 10))
    ejecutar(6, "Crear alquiler de equipo con tarifa negativa",
             lambda: crear_servicio(AlquilerEquipo, "Proyector", -20000, 2))
    ejecutar(7, "Crear servicio: asesoría especializada (válido)",
             lambda: crear_servicio(AsesoriaEspecializada, "Asesoría Python",
                                    80000, "Programación"))

    # --- Reservas (exitosas y fallidas) ---
    ejecutar(8, "Reserva exitosa: Ana + Sala Ejecutiva (3 horas)",
             lambda: crear_reserva(clientes[0], servicios[0], 3))
    ejecutar(9, "Reserva con duración inválida (0 horas)",
             lambda: crear_reserva(clientes[0], servicios[0], 0))
    ejecutar(10, "Reserva sin cliente (parámetro faltante)",
             lambda: crear_reserva(None, servicios[0], 2))

    def reserva_servicio_no_disponible():
        servicio = servicios[1]
        servicio.disponible = False  # Se marca el servicio como no disponible
        return crear_reserva(clientes[1], servicio, 2)

    ejecutar(11, "Reserva de un servicio no disponible",
             reserva_servicio_no_disponible)
    ejecutar(12, "Confirmar una reserva ya cancelada (operación no permitida)",
             reserva_cancelada_y_confirmada)

    # --- Cálculos ---
    ejecutar(13, "Cálculo de costos con métodos sobrecargados",
             costos_sobrecargados)
    ejecutar(14, "Cálculo inconsistente (descuento mayor al 100%)",
             lambda: servicios[0].calcular_costo(3, 0.19, 1.5))

    # --- Resumen final ---
    registrar_evento("Fin de la simulación")
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print(f"Operaciones exitosas: {exitosas}")
    print(f"Operaciones con error controlado: {fallidas}")
    print(f"Clientes: {len(clientes)} | Servicios: {len(servicios)} | "
          f"Reservas: {len(reservas)}")
    print("Los errores quedaron registrados en logs/sistema.log")
    print("=" * 60)


if __name__ == "__main__":
    main()
