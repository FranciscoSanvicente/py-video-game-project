"""Archivo principal para levantar el juego desde la consola.

Uso (desde PowerShell, en la raiz del proyecto):

    python main.py

Si se ejecuta con un Python que no tiene Pygame instalado (por ejemplo el
Python global del sistema), este archivo se relanza automaticamente usando el
interprete del entorno virtual ``.venv``, de modo que el juego abre igual.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DIRECTORIO_SRC = RAIZ / "src"
# Ruta al Python del entorno virtual (segun el sistema operativo).
SUBCARPETA = "Scripts" if os.name == "nt" else "bin"
EJECUTABLE = "python.exe" if os.name == "nt" else "python"
PYTHON_VENV = RAIZ / ".venv" / SUBCARPETA / EJECUTABLE


def _tiene_pygame() -> bool:
    """Indica si el interprete actual puede importar Pygame."""
    try:
        import pygame  # noqa: F401
    except ModuleNotFoundError:
        return False
    return True


def _relanzar_con_venv() -> int:
    """Vuelve a ejecutar este archivo con el Python del .venv. Devuelve su codigo."""
    usando_venv = Path(sys.executable).resolve() == PYTHON_VENV.resolve()
    if PYTHON_VENV.exists() and not usando_venv:
        return subprocess.run([str(PYTHON_VENV), str(__file__)]).returncode
    # No hay venv (o ya lo estamos usando y aun asi falta Pygame).
    print("No se encontro Pygame ni el entorno virtual .venv.")
    print("Crea el entorno e instala las dependencias con:")
    print('  python -m venv .venv')
    print(r'  .venv\Scripts\python.exe -m pip install -e ".[dev]"')
    return 1


def main() -> None:
    # Permite importar el paquete aunque no este instalado (modo desarrollo).
    sys.path.insert(0, str(DIRECTORIO_SRC))

    if not _tiene_pygame():
        raise SystemExit(_relanzar_con_venv())

    from juego_memoria.interfaz.aplicacion import Aplicacion

    Aplicacion().ejecutar()


if __name__ == "__main__":
    main()
