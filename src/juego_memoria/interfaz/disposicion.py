"""Calculo de la geometria del tablero: tamano y posicion de las cartas."""

from __future__ import annotations

import pygame

from .. import configuracion as cfg

_ALTO_HUD = 110
_MARGEN = 30


def calcular_disposicion(app, filas: int, columnas: int) -> None:
    """Calcula el tamano de carta y el origen para centrar el tablero en ``app``."""
    ancho_disponible = cfg.ANCHO_VENTANA - 2 * _MARGEN
    alto_disponible = cfg.ALTO_VENTANA - _ALTO_HUD - _MARGEN
    tam_ancho = (ancho_disponible - (columnas - 1) * app.separacion) / columnas
    tam_alto = (alto_disponible - (filas - 1) * app.separacion) / filas
    app.tamano_carta = int(min(tam_ancho, tam_alto))

    ancho_rejilla = columnas * app.tamano_carta + (columnas - 1) * app.separacion
    alto_rejilla = filas * app.tamano_carta + (filas - 1) * app.separacion
    origen_x = (cfg.ANCHO_VENTANA - ancho_rejilla) // 2
    origen_y = _ALTO_HUD + (alto_disponible - alto_rejilla) // 2
    app.origen = (origen_x, origen_y)


def rect_carta(app, fila: int, columna: int) -> pygame.Rect:
    """Rectangulo en pantalla de la carta en (fila, columna)."""
    origen_x, origen_y = app.origen
    x = origen_x + columna * (app.tamano_carta + app.separacion)
    y = origen_y + fila * (app.tamano_carta + app.separacion)
    return pygame.Rect(x, y, app.tamano_carta, app.tamano_carta)


def celda_en_pixel(app, posicion: tuple[int, int]) -> tuple[int, int] | None:
    """Convierte coordenadas de pixel en (fila, columna), o ``None``."""
    for fila in range(app.partida.tablero.filas):
        for columna in range(app.partida.tablero.columnas):
            if rect_carta(app, fila, columna).collidepoint(posicion):
                return (fila, columna)
    return None
