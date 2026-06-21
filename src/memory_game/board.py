"""Tablero del juego: la matriz bidimensional de cartas y sus operaciones."""

from __future__ import annotations

import random

from .models import Card


class Board:
    """Tablero de ``rows`` x ``cols`` cartas dispuestas en una matriz 2D.

    La matriz se guarda como una lista de listas (``grid[fila][columna]``),
    que es la estructura natural para un tablero bidimensional.
    """

    def __init__(self, rows: int, cols: int, *, seed: int | None = None) -> None:
        if (rows * cols) % 2 != 0:
            raise ValueError("El numero de casillas (filas*columnas) debe ser par.")
        self.rows = rows
        self.cols = cols
        self.grid: list[list[Card]] = self._build_grid(random.Random(seed))

    def _build_grid(self, rng: random.Random) -> list[list[Card]]:
        """Crea las parejas, las baraja y las coloca en la matriz."""
        num_pairs = (self.rows * self.cols) // 2
        # Dos cartas por cada identificador de pareja: 0,0,1,1,2,2,...
        pair_ids = [pair_id for pair_id in range(num_pairs) for _ in range(2)]
        rng.shuffle(pair_ids)

        grid: list[list[Card]] = []
        index = 0
        for r in range(self.rows):
            fila: list[Card] = []
            for c in range(self.cols):
                fila.append(Card(pair_id=pair_ids[index], row=r, col=c))
                index += 1
            grid.append(fila)
        return grid

    @property
    def num_pairs(self) -> int:
        """Cantidad total de parejas en el tablero."""
        return (self.rows * self.cols) // 2

    def in_bounds(self, row: int, col: int) -> bool:
        """Indica si (row, col) cae dentro de los limites de la matriz."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def card_at(self, row: int, col: int) -> Card:
        """Devuelve la carta en (row, col). Lanza error si esta fuera de rango."""
        if not self.in_bounds(row, col):
            raise IndexError(f"Posicion fuera del tablero: ({row}, {col})")
        return self.grid[row][col]

    def cards(self) -> list[Card]:
        """Devuelve todas las cartas en una lista plana (util para iterar)."""
        return [card for fila in self.grid for card in fila]

    def all_matched(self) -> bool:
        """``True`` cuando todas las cartas han sido emparejadas."""
        return all(card.matched for card in self.cards())
