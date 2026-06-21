"""Utilidades de dibujo compartidas por las pantallas."""

from __future__ import annotations

import pygame


def texto(pantalla: pygame.Surface, cadena: str, fuente: pygame.font.Font, color,
          *, centro=None, sup_izq=None) -> pygame.Rect:
    """Dibuja ``cadena`` en ``pantalla`` y devuelve su rectangulo.

    Se posiciona por su centro (``centro``) o por su esquina superior
    izquierda (``sup_izq``).
    """
    superficie = fuente.render(cadena, True, color)
    rectangulo = superficie.get_rect()
    if centro is not None:
        rectangulo.center = centro
    if sup_izq is not None:
        rectangulo.topleft = sup_izq
    pantalla.blit(superficie, rectangulo)
    return rectangulo
