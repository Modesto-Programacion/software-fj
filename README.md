# Software FJ - Sistema de gestión de clientes, servicios y reservas

Proyecto grupal - Programación (213023) - UNAD - Fase 4

## Reparto de responsabilidades
| Integrante | Archivos |
|---|---|
| Daniel Mendez | excepciones.py, registro.py |
| Felipe Criado | entidad.py, cliente.py |
| Lesly Chogo | servicio.py |
| Dayana Anicharico | reserva.py |
| Modesto Ovalle | main.py, informe PDF |

## Acuerdos de nombres
- Excepciones: ErrorSistema (base), ErrorValidacion, ErrorCliente,
  ErrorServicioNoDisponible, ErrorReserva, ErrorCalculo
- Logs: registrar_evento(mensaje) y registrar_error(error) -> logs/sistema.log
- Entidad (abstracta): id, describir()
- Cliente(Entidad): nombre, documento, correo, telefono (encapsulados)
- Servicio (abstracta): calcular_costo(horas, impuesto=0.19, descuento=0.0),
  describir(), validar_parametros()
- Servicios: ReservaSala, AlquilerEquipo, AsesoriaEspecializada
- Reserva: confirmar(), cancelar(), procesar()

## Cómo ejecutar
python main.py
