"""Carga de imagenes para las cartas, con respaldo (fallback) generado.

El usuario coloca sus propias imagenes (un PNG/JPG por pareja) en
``assets/images``. Si no hay suficientes, se generan automaticamente cartas
de colores con un numero, de modo que el juego SIEMPRE funciona aunque todavia
no se hayan agregado imagenes.
"""

from __future__ import annotations

import pygame

from .config import IMAGES_DIR

_SUPPORTED = (".png", ".jpg", ".jpeg", ".bmp", ".gif")

# Paleta para las cartas de respaldo (cuando faltan imagenes).
_FALLBACK_COLORS = [
    (231, 76, 60), (46, 204, 113), (52, 152, 219), (241, 196, 15),
    (155, 89, 182), (26, 188, 156), (230, 126, 34), (236, 64, 122),
    (149, 165, 166), (52, 73, 94), (39, 174, 96), (211, 84, 0),
    (127, 140, 141), (192, 57, 43), (41, 128, 185), (142, 68, 173),
    (22, 160, 133), (243, 156, 18),
]


def _list_image_files() -> list:
    """Devuelve las rutas de imagen disponibles, ordenadas por nombre."""
    if not IMAGES_DIR.exists():
        return []
    return sorted(
        p for p in IMAGES_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in _SUPPORTED
    )


def _make_fallback(pair_id: int, size: int) -> pygame.Surface:
    """Crea una carta de color con un numero, como respaldo."""
    color = _FALLBACK_COLORS[pair_id % len(_FALLBACK_COLORS)]
    surface = pygame.Surface((size, size))
    surface.fill(color)
    font = pygame.font.SysFont("arial", size // 2, bold=True)
    label = font.render(str(pair_id + 1), True, (255, 255, 255))
    rect = label.get_rect(center=(size // 2, size // 2))
    surface.blit(label, rect)
    return surface


def load_pair_images(num_pairs: int, size: int) -> dict[int, pygame.Surface]:
    """Devuelve un diccionario ``pair_id -> imagen`` escalada a ``size`` px.

    Usa las imagenes del usuario cuando existen y completa con cartas de
    respaldo cuando faltan, para cubrir las ``num_pairs`` parejas.
    """
    files = _list_image_files()
    images: dict[int, pygame.Surface] = {}
    for pair_id in range(num_pairs):
        if pair_id < len(files):
            try:
                img = pygame.image.load(str(files[pair_id])).convert_alpha()
                images[pair_id] = pygame.transform.smoothscale(img, (size, size))
                continue
            except pygame.error:
                pass  # Imagen ilegible: usamos el respaldo.
        images[pair_id] = _make_fallback(pair_id, size)
    return images
