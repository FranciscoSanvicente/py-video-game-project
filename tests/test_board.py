"""Tests del tablero (matriz 2D y generacion de parejas)."""

from __future__ import annotations

from collections import Counter

import pytest

from memory_game.board import Board


def test_dimensiones_correctas() -> None:
    board = Board(4, 6, seed=1)
    assert board.rows == 4
    assert board.cols == 6
    assert len(board.grid) == 4
    assert all(len(fila) == 6 for fila in board.grid)


def test_cada_pareja_aparece_exactamente_dos_veces() -> None:
    board = Board(4, 4, seed=42)
    conteo = Counter(card.pair_id for card in board.cards())
    assert board.num_pairs == 8
    assert all(veces == 2 for veces in conteo.values())
    assert set(conteo) == set(range(8))


def test_rechaza_tablero_impar() -> None:
    with pytest.raises(ValueError):
        Board(3, 3)


def test_in_bounds_y_card_at() -> None:
    board = Board(4, 4, seed=0)
    assert board.in_bounds(0, 0)
    assert not board.in_bounds(-1, 0)
    assert not board.in_bounds(4, 4)
    assert board.card_at(2, 3).row == 2
    with pytest.raises(IndexError):
        board.card_at(9, 9)


def test_misma_semilla_mismo_tablero() -> None:
    a = [c.pair_id for c in Board(4, 4, seed=7).cards()]
    b = [c.pair_id for c in Board(4, 4, seed=7).cards()]
    assert a == b
