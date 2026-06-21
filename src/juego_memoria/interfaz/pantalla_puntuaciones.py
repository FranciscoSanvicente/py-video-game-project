"""Pantalla de puntuaciones: tabla con los mejores 5 resultados."""

from __future__ import annotations

import pygame

from .. import configuracion as cfg
from . import estados
from .dibujo import texto


def eventos(app, evento: pygame.event.Event) -> None:
    if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
        app.estado = estados.MENU


def dibujar(app) -> None:
    centro_x = cfg.ANCHO_VENTANA // 2
    texto(app.pantalla, "Top 5 - Mejores puntuaciones", app.fuente_lg,
          cfg.COLOR_TEXTO, centro=(centro_x, 80))

    mejores = app.tabla.mejores(5)
    if not mejores:
        texto(app.pantalla, "Aun no hay puntuaciones. ¡Se el primero!",
              app.fuente_md, cfg.COLOR_TEXTO_TENUE, centro=(centro_x, 300))
    else:
        texto(app.pantalla, "#   Nombre            Mov.   Tiempo   Dificultad",
              app.fuente_sm, cfg.COLOR_TEXTO_TENUE, sup_izq=(120, 160))
        for i, p in enumerate(mejores, start=1):
            segundos = int(p.segundos)
            fila = (f"{i}   {p.nombre[:14]:<14}   {p.movimientos:>4}   "
                    f"{segundos // 60:02d}:{segundos % 60:02d}    {p.dificultad}")
            texto(app.pantalla, fila, app.fuente_sm, cfg.COLOR_TEXTO,
                  sup_izq=(120, 200 + i * 40))

    texto(app.pantalla, "Pulsa cualquier tecla para volver", app.fuente_sm,
          cfg.COLOR_TEXTO_TENUE, centro=(centro_x, 640))
