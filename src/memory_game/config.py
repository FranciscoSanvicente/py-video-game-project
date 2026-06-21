"""Constantes y configuracion global del juego.

Mantener aqui los "numeros magicos" (tamanos, colores, tiempos) hace que el
resto del codigo sea mas legible y facil de ajustar.
"""

from __future__ import annotations

from pathlib import Path

# --- Rutas -----------------------------------------------------------------
# Carpeta raiz del paquete (…/src/memory_game)
PACKAGE_DIR: Path = Path(__file__).resolve().parent
# Carpeta con las imagenes que aporta el usuario (un PNG por pareja).
IMAGES_DIR: Path = PACKAGE_DIR / "assets" / "images"
# Archivo donde se guardan los records (se crea junto a donde se ejecuta).
SCORES_FILE: Path = Path("scores.json")

# --- Dificultades ----------------------------------------------------------
# Cada dificultad define el tamano de la matriz (filas, columnas).
# El total de casillas debe ser PAR para poder formar parejas.
DIFFICULTIES: dict[str, tuple[int, int]] = {
    "Facil (4x4)": (4, 4),
    "Medio (4x6)": (4, 6),
    "Dificil (6x6)": (6, 6),
}
DEFAULT_DIFFICULTY: str = "Facil (4x4)"

# --- Ventana / render ------------------------------------------------------
WINDOW_WIDTH: int = 900
WINDOW_HEIGHT: int = 700
FPS: int = 60
TITLE: str = "Juego de Memoria"

# Tiempo (en milisegundos) que dos cartas no coincidentes permanecen visibles
# antes de volver a ocultarse.
MISMATCH_DELAY_MS: int = 800

# --- Colores (R, G, B) -----------------------------------------------------
COLOR_BG = (24, 26, 38)
COLOR_PANEL = (38, 41, 59)
COLOR_CARD_BACK = (70, 80, 130)
COLOR_CARD_FACE = (235, 238, 248)
COLOR_CARD_MATCHED = (60, 140, 95)
COLOR_TEXT = (235, 238, 248)
COLOR_TEXT_DIM = (150, 156, 180)
COLOR_ACCENT = (120, 160, 255)
COLOR_HIGHLIGHT = (255, 210, 90)
