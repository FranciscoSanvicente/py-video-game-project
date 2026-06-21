"""Pantalla de victoria: muestra el resultado y registra al ganador."""

from __future__ import annotations

import datetime

import pygame

from .. import configuracion as cfg
from ..puntuaciones import Puntuacion
from . import estados
from .dibujo import texto


def eventos(app, evento: pygame.event.Event) -> None:
    if evento.type != pygame.KEYDOWN:
        return
    if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        _guardar_ganador(app)
    elif evento.key == pygame.K_BACKSPACE:
        app.entrada_nombre = app.entrada_nombre[:-1]
    elif len(app.entrada_nombre) < 16 and evento.unicode.isprintable():
        app.entrada_nombre += evento.unicode


def _guardar_ganador(app) -> None:
    partida = app.partida
    nombre = app.entrada_nombre.strip() or "Anonimo"
    puntuacion = Puntuacion(
        nombre=nombre,
        movimientos=partida.movimientos,
        segundos=round(partida.segundos_transcurridos(), 1),
        dificultad=app.dificultad,
        fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    app.tabla.agregar(puntuacion)
    app.estado = estados.PUNTUACIONES


def dibujar(app) -> None:
    superposicion = pygame.Surface(
        (cfg.ANCHO_VENTANA, cfg.ALTO_VENTANA), pygame.SRCALPHA
    )
    superposicion.fill((0, 0, 0, 180))
    app.pantalla.blit(superposicion, (0, 0))

    centro_x = cfg.ANCHO_VENTANA // 2
    texto(app.pantalla, "¡Ganaste!", app.fuente_xl, cfg.COLOR_RESALTE,
          centro=(centro_x, 200))
    segundos = int(app.partida.segundos_transcurridos())
    resumen = f"{app.partida.movimientos} movimientos  ·  {segundos // 60:02d}:{segundos % 60:02d}"
    texto(app.pantalla, resumen, app.fuente_md, cfg.COLOR_TEXTO,
          centro=(centro_x, 270))
    texto(app.pantalla, "Escribe tu nombre:", app.fuente_md, cfg.COLOR_TEXTO_TENUE,
          centro=(centro_x, 350))

    caja = pygame.Rect(centro_x - 200, 390, 400, 56)
    pygame.draw.rect(app.pantalla, cfg.COLOR_PANEL, caja, border_radius=10)
    pygame.draw.rect(app.pantalla, cfg.COLOR_ACENTO, caja, width=2, border_radius=10)
    cursor = "|" if pygame.time.get_ticks() // 500 % 2 == 0 else ""
    texto(app.pantalla, app.entrada_nombre + cursor, app.fuente_md, cfg.COLOR_TEXTO,
          centro=caja.center)
    texto(app.pantalla, "Enter para guardar", app.fuente_sm, cfg.COLOR_TEXTO_TENUE,
          centro=(centro_x, 470))
