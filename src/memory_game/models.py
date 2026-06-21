"""Modelos de datos basicos del juego (sin dependencias de Pygame)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TurnResult(Enum):
    """Resultado de seleccionar una carta durante un turno."""

    FIRST_PICK = "first_pick"      # Se revelo la primera carta del par.
    MATCH = "match"                # Las dos cartas coinciden.
    MISMATCH = "mismatch"          # Las dos cartas son diferentes.
    INVALID = "invalid"            # Seleccion no valida (ignorar).


@dataclass
class Card:
    """Una carta del tablero.

    Attributes:
        pair_id: Identificador de la pareja. Dos cartas con el mismo
            ``pair_id`` forman un par.
        row: Fila de la carta dentro de la matriz.
        col: Columna de la carta dentro de la matriz.
        revealed: ``True`` si la carta esta boca arriba en este momento.
        matched: ``True`` si la carta ya fue emparejada correctamente.
    """

    pair_id: int
    row: int
    col: int
    revealed: bool = False
    matched: bool = False

    @property
    def face_up(self) -> bool:
        """La carta se ve boca arriba si esta revelada o ya emparejada."""
        return self.revealed or self.matched
