"""Tests de la logica de turnos (Game)."""

from __future__ import annotations

from memory_game.game import Game
from memory_game.models import TurnResult


def _posiciones_por_pareja(game: Game) -> dict[int, list[tuple[int, int]]]:
    """Mapa pair_id -> lista de (fila, col), para localizar pares en los tests."""
    mapa: dict[int, list[tuple[int, int]]] = {}
    for card in game.board.cards():
        mapa.setdefault(card.pair_id, []).append((card.row, card.col))
    return mapa


def test_primera_seleccion() -> None:
    game = Game(4, 4, seed=1)
    (r, c) = (0, 0)
    assert game.select(r, c) == TurnResult.FIRST_PICK
    assert game.board.card_at(r, c).revealed
    assert game.moves == 0  # El movimiento se cuenta al elegir la segunda carta.


def test_match_marca_ambas_y_suma_movimiento() -> None:
    game = Game(4, 4, seed=1)
    pos = _posiciones_por_pareja(game)
    (a, b) = pos[0]  # Dos cartas de la pareja 0.
    assert game.select(*a) == TurnResult.FIRST_PICK
    assert game.select(*b) == TurnResult.MATCH
    assert game.board.card_at(*a).matched
    assert game.board.card_at(*b).matched
    assert game.moves == 1


def test_mismatch_y_resolucion() -> None:
    game = Game(4, 4, seed=1)
    pos = _posiciones_por_pareja(game)
    primera = pos[0][0]
    segunda = pos[1][0]  # Pareja distinta.
    assert game.select(*primera) == TurnResult.FIRST_PICK
    assert game.select(*segunda) == TurnResult.MISMATCH
    assert game.waiting_for_mismatch
    # Mientras se muestran las dos, otras jugadas se ignoran.
    assert game.select(0, 0) == TurnResult.INVALID
    game.resolve_mismatch()
    assert not game.board.card_at(*primera).revealed
    assert not game.board.card_at(*segunda).revealed
    assert not game.waiting_for_mismatch


def test_no_se_puede_elegir_carta_ya_revelada() -> None:
    game = Game(4, 4, seed=3)
    assert game.select(0, 0) == TurnResult.FIRST_PICK
    assert game.select(0, 0) == TurnResult.INVALID


def test_seleccion_fuera_de_limites() -> None:
    game = Game(4, 4, seed=3)
    assert game.select(99, 99) == TurnResult.INVALID


def test_ganar_emparejando_todo() -> None:
    game = Game(4, 4, seed=5)
    for posiciones in _posiciones_por_pareja(game).values():
        game.select(*posiciones[0])
        game.select(*posiciones[1])
    assert game.won
    assert game.moves == game.board.num_pairs


def test_tiempo_se_congela_al_ganar() -> None:
    reloj = {"t": 0.0}
    game = Game(4, 4, seed=5, clock=lambda: reloj["t"])
    for posiciones in _posiciones_por_pareja(game).values():
        reloj["t"] += 1.0
        game.select(*posiciones[0])
        game.select(*posiciones[1])
    tiempo_final = game.elapsed_seconds()
    reloj["t"] += 100.0  # El tiempo externo avanza...
    assert game.elapsed_seconds() == tiempo_final  # ...pero el de la partida no.
