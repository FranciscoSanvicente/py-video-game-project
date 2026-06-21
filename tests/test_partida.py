"""Tests de la logica de turnos (Partida)."""

from __future__ import annotations

from juego_memoria.modelos import ResultadoTurno
from juego_memoria.partida import Partida


def _posiciones_por_pareja(partida: Partida) -> dict[int, list[tuple[int, int]]]:
    """Mapa id_pareja -> lista de (fila, col), para localizar pares en los tests."""
    mapa: dict[int, list[tuple[int, int]]] = {}
    for carta in partida.tablero.cartas():
        mapa.setdefault(carta.id_pareja, []).append((carta.fila, carta.columna))
    return mapa


def test_primera_seleccion() -> None:
    partida = Partida(4, 4, semilla=1)
    assert partida.seleccionar(0, 0) == ResultadoTurno.PRIMERA
    assert partida.tablero.carta_en(0, 0).revelada
    assert partida.movimientos == 0  # El movimiento se cuenta en la segunda carta.


def test_pareja_marca_ambas_y_suma_movimiento() -> None:
    partida = Partida(4, 4, semilla=1)
    posiciones = _posiciones_por_pareja(partida)
    a, b = posiciones[0]
    assert partida.seleccionar(*a) == ResultadoTurno.PRIMERA
    assert partida.seleccionar(*b) == ResultadoTurno.PAREJA
    assert partida.tablero.carta_en(*a).emparejada
    assert partida.tablero.carta_en(*b).emparejada
    assert partida.movimientos == 1


def test_desajuste_y_resolucion() -> None:
    partida = Partida(4, 4, semilla=1)
    posiciones = _posiciones_por_pareja(partida)
    primera = posiciones[0][0]
    segunda = posiciones[1][0]  # Pareja distinta.
    assert partida.seleccionar(*primera) == ResultadoTurno.PRIMERA
    assert partida.seleccionar(*segunda) == ResultadoTurno.DESAJUSTE
    assert partida.esperando_desajuste
    # Mientras se muestran las dos, otras jugadas se ignoran.
    assert partida.seleccionar(0, 0) == ResultadoTurno.INVALIDO
    partida.resolver_desajuste()
    assert not partida.tablero.carta_en(*primera).revelada
    assert not partida.tablero.carta_en(*segunda).revelada
    assert not partida.esperando_desajuste


def test_no_se_puede_elegir_carta_ya_revelada() -> None:
    partida = Partida(4, 4, semilla=3)
    assert partida.seleccionar(0, 0) == ResultadoTurno.PRIMERA
    assert partida.seleccionar(0, 0) == ResultadoTurno.INVALIDO


def test_seleccion_fuera_de_limites() -> None:
    partida = Partida(4, 4, semilla=3)
    assert partida.seleccionar(99, 99) == ResultadoTurno.INVALIDO


def test_ganar_emparejando_todo() -> None:
    partida = Partida(4, 4, semilla=5)
    for posiciones in _posiciones_por_pareja(partida).values():
        partida.seleccionar(*posiciones[0])
        partida.seleccionar(*posiciones[1])
    assert partida.ganada
    assert partida.movimientos == partida.tablero.num_parejas


def test_tiempo_se_congela_al_ganar() -> None:
    reloj = {"t": 0.0}
    partida = Partida(4, 4, semilla=5, reloj=lambda: reloj["t"])
    for posiciones in _posiciones_por_pareja(partida).values():
        reloj["t"] += 1.0
        partida.seleccionar(*posiciones[0])
        partida.seleccionar(*posiciones[1])
    tiempo_final = partida.segundos_transcurridos()
    reloj["t"] += 100.0  # El tiempo externo avanza...
    assert partida.segundos_transcurridos() == tiempo_final  # ...el de la partida no.
