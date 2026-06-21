"""Persistencia de records: guardar y leer las mejores puntuaciones.

El historial se guarda en un archivo JSON (formato libre segun la guia).
Cada record almacena el nombre del jugador, los movimientos, el tiempo en
segundos, la dificultad y la fecha. El "mejor" resultado es el que usa menos
movimientos y, a igualdad de movimientos, menos tiempo.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import SCORES_FILE


@dataclass
class Score:
    """Una entrada en la tabla de records."""

    name: str
    moves: int
    seconds: float
    difficulty: str
    date: str

    def sort_key(self) -> tuple[int, float]:
        """Menos movimientos primero; a igualdad, menos tiempo."""
        return (self.moves, self.seconds)


class ScoreBoard:
    """Tabla de records persistida en disco."""

    def __init__(self, path: Path = SCORES_FILE) -> None:
        self.path = Path(path)
        self.scores: list[Score] = self._load()

    def _load(self) -> list[Score]:
        """Lee los records del archivo. Si no existe o esta danado, lista vacia."""
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            return [Score(**item) for item in raw]
        except (json.JSONDecodeError, TypeError, ValueError):
            # Archivo corrupto: no rompemos el juego, empezamos limpio.
            return []

    def save(self) -> None:
        """Escribe todos los records en el archivo JSON."""
        data = [asdict(score) for score in self.scores]
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add(self, score: Score) -> None:
        """Agrega un record y guarda inmediatamente en disco."""
        self.scores.append(score)
        self.save()

    def top(self, limit: int = 5) -> list[Score]:
        """Devuelve los mejores ``limit`` records ya ordenados."""
        return sorted(self.scores, key=Score.sort_key)[:limit]

    def is_high_score(self, moves: int, seconds: float, limit: int = 5) -> bool:
        """Indica si (moves, seconds) entraria en el Top ``limit``."""
        best = self.top(limit)
        if len(best) < limit:
            return True
        return (moves, seconds) < best[-1].sort_key()
