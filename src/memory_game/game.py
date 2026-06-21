"""Logica de la partida: turnos, validacion, conteo de movimientos y tiempo.

Esta clase NO sabe nada de Pygame. Recibe selecciones de cartas (fila,
columna) y devuelve el resultado del turno. Asi puede probarse con tests
automaticos sin abrir ninguna ventana.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from .board import Board
from .models import Card, TurnResult


class Game:
    """Coordina una partida del juego de memoria."""

    def __init__(self, rows: int, cols: int, *, seed: int | None = None,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.board = Board(rows, cols, seed=seed)
        self._clock = clock                 # Funcion de reloj (inyectable en tests).
        self.moves: int = 0                 # Numero de pares intentados.
        self.first: Card | None = None      # Primera carta revelada del turno.
        self.second: Card | None = None     # Segunda carta (cuando hay desajuste).
        self._start_time: float = self._clock()
        self._end_time: float | None = None

    # --- Tiempo ------------------------------------------------------------
    def elapsed_seconds(self) -> float:
        """Segundos transcurridos desde el inicio (se congela al ganar)."""
        end = self._end_time if self._end_time is not None else self._clock()
        return end - self._start_time

    # --- Estado ------------------------------------------------------------
    @property
    def waiting_for_mismatch(self) -> bool:
        """``True`` si hay dos cartas no coincidentes esperando ocultarse."""
        return self.second is not None

    @property
    def won(self) -> bool:
        """``True`` cuando se han emparejado todas las cartas."""
        return self.board.all_matched()

    # --- Acciones del jugador ---------------------------------------------
    def select(self, row: int, col: int) -> TurnResult:
        """Procesa la seleccion de la carta en (row, col).

        Devuelve un :class:`TurnResult` describiendo lo ocurrido. Las
        selecciones invalidas (fuera de limites, carta ya revelada o
        emparejada, o mientras se muestran dos cartas) se ignoran.
        """
        # No aceptar jugadas mientras dos cartas no coincidentes siguen visibles.
        if self.waiting_for_mismatch or self.won:
            return TurnResult.INVALID
        if not self.board.in_bounds(row, col):
            return TurnResult.INVALID

        card = self.board.card_at(row, col)
        # No se puede elegir una carta ya emparejada ni la ya revelada.
        if card.matched or card.revealed:
            return TurnResult.INVALID

        card.revealed = True

        # Primera carta del turno.
        if self.first is None:
            self.first = card
            return TurnResult.FIRST_PICK

        # Segunda carta: contamos el movimiento y comparamos.
        self.moves += 1
        if card.pair_id == self.first.pair_id:
            self.first.matched = True
            card.matched = True
            self.first = None
            if self.won:
                self._end_time = self._clock()
            return TurnResult.MATCH

        # No coinciden: quedan visibles hasta que se llame a resolve_mismatch().
        self.second = card
        return TurnResult.MISMATCH

    def resolve_mismatch(self) -> None:
        """Oculta las dos cartas no coincidentes y termina el turno.

        La interfaz llama a esto tras una breve pausa para que el jugador
        alcance a memorizarlas.
        """
        if self.first is not None:
            self.first.revealed = False
        if self.second is not None:
            self.second.revealed = False
        self.first = None
        self.second = None
