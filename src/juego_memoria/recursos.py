"""Carga de imagenes para las cartas, con respaldo (fallback) generado.

El usuario coloca sus propias imagenes (un archivo por pareja) en
``recursos/imagenes``. Si no hay suficientes, se generan automaticamente
cartas de colores con un numero, de modo que el juego SIEMPRE funciona aunque
todavia no se hayan agregado imagenes.
"""

from __future__ import annotations

import pygame

from .configuracion import DIRECTORIO_IMAGENES

_FORMATOS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")

# Paleta para las cartas de respaldo (cuando faltan imagenes).
_COLORES_RESPALDO = [
    (231, 76, 60), (46, 204, 113), (52, 152, 219), (241, 196, 15),
    (155, 89, 182), (26, 188, 156), (230, 126, 34), (236, 64, 122),
    (149, 165, 166), (52, 73, 94), (39, 174, 96), (211, 84, 0),
    (127, 140, 141), (192, 57, 43), (41, 128, 185), (142, 68, 173),
    (22, 160, 133), (243, 156, 18),
]


def _listar_archivos_imagen() -> list:
    """Devuelve las rutas de imagen disponibles, ordenadas por nombre."""
    if not DIRECTORIO_IMAGENES.exists():
        return []
    return sorted(
        ruta for ruta in DIRECTORIO_IMAGENES.iterdir()
        if ruta.is_file() and ruta.suffix.lower() in _FORMATOS
    )


def _crear_respaldo(id_pareja: int, tamano: int) -> pygame.Surface:
    """Crea una carta de color con un numero, como respaldo."""
    color = _COLORES_RESPALDO[id_pareja % len(_COLORES_RESPALDO)]
    superficie = pygame.Surface((tamano, tamano))
    superficie.fill(color)
    fuente = pygame.font.SysFont("arial", tamano // 2, bold=True)
    etiqueta = fuente.render(str(id_pareja + 1), True, (255, 255, 255))
    rectangulo = etiqueta.get_rect(center=(tamano // 2, tamano // 2))
    superficie.blit(etiqueta, rectangulo)
    return superficie


def cargar_imagenes_parejas(num_parejas: int, tamano: int) -> dict[int, pygame.Surface]:
    """Devuelve un diccionario ``id_pareja -> imagen`` escalada a ``tamano`` px.

    Usa las imagenes del usuario cuando existen y completa con cartas de
    respaldo cuando faltan, para cubrir las ``num_parejas`` parejas.
    """
    archivos = _listar_archivos_imagen()
    imagenes: dict[int, pygame.Surface] = {}
    for id_pareja in range(num_parejas):
        if id_pareja < len(archivos):
            try:
                imagen = pygame.image.load(str(archivos[id_pareja])).convert_alpha()
                imagenes[id_pareja] = pygame.transform.smoothscale(imagen, (tamano, tamano))
                continue
            except pygame.error:
                pass  # Imagen ilegible: usamos el respaldo.
        imagenes[id_pareja] = _crear_respaldo(id_pareja, tamano)
    return imagenes
