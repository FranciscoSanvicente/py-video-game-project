"""Pantalla de menu: elegir dificultad, jugar o ver puntuaciones."""

from __future__ import annotations

import pygame

from .. import configuracion as cfg
from . import estados
from .dibujo import texto


def _rects_dificultad() -> list[pygame.Rect]:
    return [
        pygame.Rect(cfg.ANCHO_VENTANA // 2 - 170, 250 + i * 64, 340, 52)
        for i in range(len(cfg.DIFICULTADES))
    ]


def _rect_jugar() -> pygame.Rect:
    return pygame.Rect(cfg.ANCHO_VENTANA // 2 - 170, 480, 340, 56)


def _rect_puntuaciones() -> pygame.Rect:
    return pygame.Rect(cfg.ANCHO_VENTANA // 2 - 170, 548, 340, 48)


def eventos(app, evento: pygame.event.Event) -> None:
    nombres = list(cfg.DIFICULTADES)
    if evento.type == pygame.KEYDOWN:
        if evento.key in (pygame.K_UP, pygame.K_LEFT):
            i = nombres.index(app.dificultad)
            app.dificultad = nombres[(i - 1) % len(nombres)]
        elif evento.key in (pygame.K_DOWN, pygame.K_RIGHT):
            i = nombres.index(app.dificultad)
            app.dificultad = nombres[(i + 1) % len(nombres)]
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            app.iniciar_partida()
        elif evento.key == pygame.K_p:
            app.estado = estados.PUNTUACIONES
        elif evento.key == pygame.K_ESCAPE:
            app.ejecutando = False
    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        for i, rect in enumerate(_rects_dificultad()):
            if rect.collidepoint(evento.pos):
                app.dificultad = nombres[i]
        if _rect_jugar().collidepoint(evento.pos):
            app.iniciar_partida()
        elif _rect_puntuaciones().collidepoint(evento.pos):
            app.estado = estados.PUNTUACIONES


def dibujar(app) -> None:
    centro_x = cfg.ANCHO_VENTANA // 2
    texto(app.pantalla, "Juego de Memoria", app.fuente_xl, cfg.COLOR_TEXTO,
          centro=(centro_x, 120))
    texto(app.pantalla, "Elige la dificultad", app.fuente_md, cfg.COLOR_TEXTO_TENUE,
          centro=(centro_x, 205))

    nombres = list(cfg.DIFICULTADES)
    for rect, nombre in zip(_rects_dificultad(), nombres, strict=True):
        seleccionada = nombre == app.dificultad
        color = cfg.COLOR_ACENTO if seleccionada else cfg.COLOR_PANEL
        pygame.draw.rect(app.pantalla, color, rect, border_radius=10)
        texto(app.pantalla, nombre, app.fuente_md, cfg.COLOR_TEXTO, centro=rect.center)

    jugar = _rect_jugar()
    pygame.draw.rect(app.pantalla, cfg.COLOR_CARTA_EMPAREJADA, jugar, border_radius=10)
    texto(app.pantalla, "JUGAR  (Enter)", app.fuente_md, cfg.COLOR_TEXTO,
          centro=jugar.center)

    puntuaciones = _rect_puntuaciones()
    pygame.draw.rect(app.pantalla, cfg.COLOR_PANEL, puntuaciones, border_radius=10)
    texto(app.pantalla, "Mejores puntuaciones  (P)", app.fuente_sm, cfg.COLOR_TEXTO,
          centro=puntuaciones.center)

    texto(app.pantalla, "Flechas: cambiar  ·  Esc: salir", app.fuente_sm,
          cfg.COLOR_TEXTO_TENUE, centro=(centro_x, 640))
