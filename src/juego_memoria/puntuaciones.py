"""Persistencia de puntuaciones: guardar y leer los mejores resultados.

El historial se guarda en un archivo JSON (formato libre segun la guia).
Cada puntuacion almacena el nombre del jugador, los movimientos, el tiempo en
segundos, la dificultad y la fecha. El "mejor" resultado es el que usa menos
movimientos y, a igualdad de movimientos, menos tiempo.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .configuracion import ARCHIVO_PUNTUACIONES


@dataclass
class Puntuacion:
    """Una entrada en la tabla de puntuaciones."""

    nombre: str
    movimientos: int
    segundos: float
    dificultad: str
    fecha: str

    def clave_orden(self) -> tuple[int, float]:
        """Menos movimientos primero; a igualdad, menos tiempo."""
        return (self.movimientos, self.segundos)


class TablaPuntuaciones:
    """Tabla de puntuaciones persistida en disco."""

    def __init__(self, ruta: Path = ARCHIVO_PUNTUACIONES) -> None:
        self.ruta = Path(ruta)
        self.puntuaciones: list[Puntuacion] = self._cargar()

    def _cargar(self) -> list[Puntuacion]:
        """Lee las puntuaciones. Si no existe o esta danada, lista vacia."""
        if not self.ruta.exists():
            return []
        try:
            datos = json.loads(self.ruta.read_text(encoding="utf-8"))
            return [Puntuacion(**item) for item in datos]
        except (json.JSONDecodeError, TypeError, ValueError):
            # Archivo corrupto: no rompemos el juego, empezamos limpio.
            return []

    def guardar(self) -> None:
        """Escribe todas las puntuaciones en el archivo JSON."""
        datos = [asdict(puntuacion) for puntuacion in self.puntuaciones]
        self.ruta.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def agregar(self, puntuacion: Puntuacion) -> None:
        """Agrega una puntuacion y guarda inmediatamente en disco."""
        self.puntuaciones.append(puntuacion)
        self.guardar()

    def mejores(self, limite: int = 5) -> list[Puntuacion]:
        """Devuelve las mejores ``limite`` puntuaciones ya ordenadas."""
        return sorted(self.puntuaciones, key=Puntuacion.clave_orden)[:limite]

    def es_record(self, movimientos: int, segundos: float, limite: int = 5) -> bool:
        """Indica si (movimientos, segundos) entraria en el Top ``limite``."""
        mejores = self.mejores(limite)
        if len(mejores) < limite:
            return True
        return (movimientos, segundos) < mejores[-1].clave_orden()
