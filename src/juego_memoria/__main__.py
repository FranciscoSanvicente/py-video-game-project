"""Punto de entrada: ``python -m juego_memoria``."""

from __future__ import annotations

from .interfaz.aplicacion import Aplicacion


def main() -> None:
    Aplicacion().ejecutar()


if __name__ == "__main__":
    main()
