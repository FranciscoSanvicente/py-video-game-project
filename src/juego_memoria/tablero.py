"""Tablero del juego: la matriz bidimensional de cartas y sus operaciones."""

from __future__ import annotations

import random

from .modelos import Carta


class Tablero:
    """Tablero de ``filas`` x ``columnas`` cartas dispuestas en una matriz 2D.

    La matriz se guarda como una lista de listas (``matriz[fila][columna]``),
    que es la estructura natural para un tablero bidimensional.
    """

    def __init__(self, filas: int, columnas: int, *, semilla: int | None = None) -> None:
        if (filas * columnas) % 2 != 0:
            raise ValueError("El numero de casillas (filas*columnas) debe ser par.")
        self.filas = filas
        self.columnas = columnas
        self.matriz: list[list[Carta]] = self._construir_matriz(random.Random(semilla))

    def _construir_matriz(self, generador: random.Random) -> list[list[Carta]]:
        """Crea las parejas, las baraja y las coloca en la matriz."""
        # Dos cartas por cada identificador de pareja: 0,0,1,1,2,2,...
        identificadores = [pareja for pareja in range(self.num_parejas) for _ in range(2)]
        generador.shuffle(identificadores)

        matriz: list[list[Carta]] = []
        indice = 0
        for fila in range(self.filas):
            fila_cartas: list[Carta] = []
            for columna in range(self.columnas):
                fila_cartas.append(Carta(id_pareja=identificadores[indice],
                                         fila=fila, columna=columna))
                indice += 1
            matriz.append(fila_cartas)
        return matriz

    @property
    def num_parejas(self) -> int:
        """Cantidad total de parejas en el tablero."""
        return (self.filas * self.columnas) // 2

    def dentro_limites(self, fila: int, columna: int) -> bool:
        """Indica si (fila, columna) cae dentro de los limites de la matriz."""
        return 0 <= fila < self.filas and 0 <= columna < self.columnas

    def carta_en(self, fila: int, columna: int) -> Carta:
        """Devuelve la carta en (fila, columna). Error si esta fuera de rango."""
        if not self.dentro_limites(fila, columna):
            raise IndexError(f"Posicion fuera del tablero: ({fila}, {columna})")
        return self.matriz[fila][columna]

    def cartas(self) -> list[Carta]:
        """Devuelve todas las cartas en una lista plana (util para iterar)."""
        return [carta for fila in self.matriz for carta in fila]

    def todas_emparejadas(self) -> bool:
        """``True`` cuando todas las cartas han sido emparejadas."""
        return all(carta.emparejada for carta in self.cartas())
