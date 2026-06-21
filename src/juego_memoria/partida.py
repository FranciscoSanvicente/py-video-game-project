"""Logica de la partida: turnos, validacion, conteo de movimientos y tiempo.

Esta clase NO sabe nada de Pygame. Recibe selecciones de cartas (fila,
columna) y devuelve el resultado del turno. Asi puede probarse con tests
automaticos sin abrir ninguna ventana.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from .modelos import Carta, ResultadoTurno
from .tablero import Tablero


class Partida:
    """Coordina una partida del juego de memoria."""

    def __init__(self, filas: int, columnas: int, *, semilla: int | None = None,
                 reloj: Callable[[], float] = time.monotonic) -> None:
        self.tablero = Tablero(filas, columnas, semilla=semilla)
        self._reloj = reloj                 # Funcion de reloj (inyectable en tests).
        self.movimientos: int = 0           # Numero de parejas intentadas.
        self.primera: Carta | None = None   # Primera carta revelada del turno.
        self.segunda: Carta | None = None    # Segunda carta (cuando hay desajuste).
        self._tiempo_inicio: float = self._reloj()
        self._tiempo_fin: float | None = None

    # --- Tiempo ------------------------------------------------------------
    def segundos_transcurridos(self) -> float:
        """Segundos transcurridos desde el inicio (se congela al ganar)."""
        fin = self._tiempo_fin if self._tiempo_fin is not None else self._reloj()
        return fin - self._tiempo_inicio

    # --- Estado ------------------------------------------------------------
    @property
    def esperando_desajuste(self) -> bool:
        """``True`` si hay dos cartas no coincidentes esperando ocultarse."""
        return self.segunda is not None

    @property
    def ganada(self) -> bool:
        """``True`` cuando se han emparejado todas las cartas."""
        return self.tablero.todas_emparejadas()

    # --- Acciones del jugador ---------------------------------------------
    def seleccionar(self, fila: int, columna: int) -> ResultadoTurno:
        """Procesa la seleccion de la carta en (fila, columna).

        Devuelve un :class:`ResultadoTurno` describiendo lo ocurrido. Las
        selecciones invalidas (fuera de limites, carta ya revelada o
        emparejada, o mientras se muestran dos cartas) se ignoran.
        """
        # No aceptar jugadas mientras dos cartas no coincidentes siguen visibles.
        if self.esperando_desajuste or self.ganada:
            return ResultadoTurno.INVALIDO
        if not self.tablero.dentro_limites(fila, columna):
            return ResultadoTurno.INVALIDO

        carta = self.tablero.carta_en(fila, columna)
        # No se puede elegir una carta ya emparejada ni la ya revelada.
        if carta.emparejada or carta.revelada:
            return ResultadoTurno.INVALIDO

        carta.revelada = True

        # Primera carta del turno.
        if self.primera is None:
            self.primera = carta
            return ResultadoTurno.PRIMERA

        # Segunda carta: contamos el movimiento y comparamos.
        self.movimientos += 1
        if carta.id_pareja == self.primera.id_pareja:
            self.primera.emparejada = True
            carta.emparejada = True
            self.primera = None
            if self.ganada:
                self._tiempo_fin = self._reloj()
            return ResultadoTurno.PAREJA

        # No coinciden: quedan visibles hasta que se llame a resolver_desajuste().
        self.segunda = carta
        return ResultadoTurno.DESAJUSTE

    def resolver_desajuste(self) -> None:
        """Oculta las dos cartas no coincidentes y termina el turno.

        La interfaz llama a esto tras una breve pausa para que el jugador
        alcance a memorizarlas.
        """
        if self.primera is not None:
            self.primera.revelada = False
        if self.segunda is not None:
            self.segunda.revelada = False
        self.primera = None
        self.segunda = None
