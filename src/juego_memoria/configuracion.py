"""Constantes y configuracion global del juego.

Mantener aqui los "numeros magicos" (tamanos, colores, tiempos) hace que el
resto del codigo sea mas legible y facil de ajustar.
"""

from __future__ import annotations

from pathlib import Path

# --- Rutas -----------------------------------------------------------------
# Carpeta raiz del paquete (…/src/juego_memoria)
DIRECTORIO_PAQUETE: Path = Path(__file__).resolve().parent
# Carpeta con las imagenes que aporta el usuario (un archivo por pareja).
DIRECTORIO_IMAGENES: Path = DIRECTORIO_PAQUETE / "recursos" / "imagenes"
# Carpeta con los efectos de sonido (.wav).
DIRECTORIO_SONIDOS: Path = DIRECTORIO_PAQUETE / "recursos" / "sonidos"
# Archivo donde se guardan las puntuaciones (se crea junto a donde se ejecuta).
ARCHIVO_PUNTUACIONES: Path = Path("puntuaciones.json")

# --- Dificultades ----------------------------------------------------------
# Cada dificultad define el tamano de la matriz (filas, columnas).
# El total de casillas debe ser PAR para poder formar parejas.
DIFICULTADES: dict[str, tuple[int, int]] = {
    "Facil (4x4)": (4, 4),
    "Medio (4x6)": (4, 6),
    "Dificil (6x6)": (6, 6),
}
DIFICULTAD_PREDETERMINADA: str = "Facil (4x4)"

# --- Ventana / dibujo ------------------------------------------------------
ANCHO_VENTANA: int = 900
ALTO_VENTANA: int = 700
FPS: int = 60
TITULO: str = "Juego de Memoria"

# Tiempo (en milisegundos) que dos cartas no coincidentes permanecen visibles
# antes de volver a ocultarse.
RETARDO_DESAJUSTE_MS: int = 800

# --- Colores (R, G, B) -----------------------------------------------------
COLOR_FONDO = (24, 26, 38)
COLOR_PANEL = (38, 41, 59)
COLOR_CARTA_DORSO = (70, 80, 130)
COLOR_CARTA_FRENTE = (235, 238, 248)
COLOR_CARTA_EMPAREJADA = (60, 140, 95)
COLOR_TEXTO = (235, 238, 248)
COLOR_TEXTO_TENUE = (150, 156, 180)
COLOR_ACENTO = (120, 160, 255)
COLOR_RESALTE = (255, 210, 90)
