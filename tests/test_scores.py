"""Tests de la tabla de records (persistencia y ordenamiento)."""

from __future__ import annotations

from memory_game.scores import Score, ScoreBoard


def _score(name: str, moves: int, seconds: float) -> Score:
    return Score(name=name, moves=moves, seconds=seconds,
                 difficulty="Facil (4x4)", date="2026-01-01 10:00")


def test_guarda_y_recarga(tmp_path) -> None:
    archivo = tmp_path / "scores.json"
    tablero = ScoreBoard(archivo)
    tablero.add(_score("Ana", 10, 45.0))
    # Una nueva instancia debe leer lo guardado en disco.
    recargado = ScoreBoard(archivo)
    assert len(recargado.scores) == 1
    assert recargado.scores[0].name == "Ana"


def test_orden_por_movimientos_luego_tiempo(tmp_path) -> None:
    tablero = ScoreBoard(tmp_path / "s.json")
    tablero.add(_score("Lento", 10, 100.0))
    tablero.add(_score("Rapido", 5, 80.0))
    tablero.add(_score("Empate", 5, 50.0))
    top = tablero.top(5)
    assert [s.name for s in top] == ["Empate", "Rapido", "Lento"]


def test_top_limita_resultados(tmp_path) -> None:
    tablero = ScoreBoard(tmp_path / "s.json")
    for i in range(8):
        tablero.add(_score(f"J{i}", i + 1, 10.0))
    assert len(tablero.top(5)) == 5


def test_is_high_score(tmp_path) -> None:
    tablero = ScoreBoard(tmp_path / "s.json")
    for i in range(5):
        tablero.add(_score(f"J{i}", 10 + i, 10.0))  # 10..14 movimientos
    assert tablero.is_high_score(8, 10.0)    # Mejor que el peor (14).
    assert not tablero.is_high_score(20, 5.0)  # Peor que todos.


def test_archivo_corrupto_no_rompe(tmp_path) -> None:
    archivo = tmp_path / "s.json"
    archivo.write_text("esto no es json valido {", encoding="utf-8")
    tablero = ScoreBoard(archivo)  # No debe lanzar excepcion.
    assert tablero.scores == []
