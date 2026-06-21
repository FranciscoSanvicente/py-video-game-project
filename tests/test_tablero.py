"""Tests del tablero (matriz 2D y generacion de parejas)."""

from __future__ import annotations

from collections import Counter

import pytest

from juego_memoria.tablero import Tablero


def test_dimensiones_correctas() -> None:
    tablero = Tablero(4, 6, semilla=1)
    assert tablero.filas == 4
    assert tablero.columnas == 6
    assert len(tablero.matriz) == 4
    assert all(len(fila) == 6 for fila in tablero.matriz)


def test_cada_pareja_aparece_exactamente_dos_veces() -> None:
    tablero = Tablero(4, 4, semilla=42)
    conteo = Counter(carta.id_pareja for carta in tablero.cartas())
    assert tablero.num_parejas == 8
    assert all(veces == 2 for veces in conteo.values())
    assert set(conteo) == set(range(8))


def test_rechaza_tablero_impar() -> None:
    with pytest.raises(ValueError):
        Tablero(3, 3)


def test_dentro_limites_y_carta_en() -> None:
    tablero = Tablero(4, 4, semilla=0)
    assert tablero.dentro_limites(0, 0)
    assert not tablero.dentro_limites(-1, 0)
    assert not tablero.dentro_limites(4, 4)
    assert tablero.carta_en(2, 3).fila == 2
    with pytest.raises(IndexError):
        tablero.carta_en(9, 9)


def test_misma_semilla_mismo_tablero() -> None:
    a = [c.id_pareja for c in Tablero(4, 4, semilla=7).cartas()]
    b = [c.id_pareja for c in Tablero(4, 4, semilla=7).cartas()]
    assert a == b
