"""Modelos de datos basicos del juego (sin dependencias de Pygame)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ResultadoTurno(Enum):
    """Resultado de seleccionar una carta durante un turno."""

    PRIMERA = "primera"        # Se revelo la primera carta del par.
    PAREJA = "pareja"          # Las dos cartas coinciden.
    DESAJUSTE = "desajuste"    # Las dos cartas son diferentes.
    INVALIDO = "invalido"      # Seleccion no valida (ignorar).


@dataclass
class Carta:
    """Una carta del tablero.

    Attributes:
        id_pareja: Identificador de la pareja. Dos cartas con el mismo
            ``id_pareja`` forman un par.
        fila: Fila de la carta dentro de la matriz.
        columna: Columna de la carta dentro de la matriz.
        revelada: ``True`` si la carta esta boca arriba en este momento.
        emparejada: ``True`` si la carta ya fue emparejada correctamente.
    """

    id_pareja: int
    fila: int
    columna: int
    revelada: bool = False
    emparejada: bool = False

    @property
    def boca_arriba(self) -> bool:
        """La carta se ve boca arriba si esta revelada o ya emparejada."""
        return self.revelada or self.emparejada
