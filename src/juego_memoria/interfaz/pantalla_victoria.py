"""Pantalla de victoria: muestra el resultado y registra al ganador.

El jugador puede escribir un nombre nuevo o elegir con un clic uno de los
nombres ya usados en partidas anteriores.
"""

from __future__ import annotations

import datetime

import pygame

from .. import configuracion as cfg
from ..puntuaciones import Puntuacion
from . import estados
from .dibujo import texto


def _nombres_existentes(app, limite: int = 6) -> list[str]:
    """Nombres unicos ya registrados, del mas reciente al mas antiguo."""
    unicos: list[str] = []
    for puntuacion in reversed(app.tabla.puntuaciones):
        if puntuacion.nombre not in unicos:
            unicos.append(puntuacion.nombre)
        if len(unicos) >= limite:
            break
    return unicos


def _rects_nombres(nombres: list[str]) -> list[tuple[pygame.Rect, str]]:
    """Rectangulos (en 2 columnas) para los botones de nombres existentes."""
    centro_x = cfg.ANCHO_VENTANA // 2
    ancho, alto, separacion = 180, 40, 16
    rects: list[tuple[pygame.Rect, str]] = []
    for i, nombre in enumerate(nombres):
        fila, columna = divmod(i, 2)
        x = centro_x - ancho - separacion // 2 + columna * (ancho + separacion)
        y = 478 + fila * (alto + 12)
        rects.append((pygame.Rect(x, y, ancho, alto), nombre))
    return rects


def eventos(app, evento: pygame.event.Event) -> None:
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        for rect, nombre in _rects_nombres(_nombres_existentes(app)):
            if rect.collidepoint(evento.pos):
                app.entrada_nombre = nombre
                _guardar_ganador(app)
                return
    elif evento.type == pygame.KEYDOWN:
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
          centro=(centro_x, 170))
    segundos = int(app.partida.segundos_transcurridos())
    resumen = f"{app.partida.movimientos} movimientos  ·  {segundos // 60:02d}:{segundos % 60:02d}"
    texto(app.pantalla, resumen, app.fuente_md, cfg.COLOR_TEXTO,
          centro=(centro_x, 228))
    texto(app.pantalla, "Escribe tu nombre:", app.fuente_md, cfg.COLOR_TEXTO_TENUE,
          centro=(centro_x, 285))

    caja = pygame.Rect(centro_x - 200, 315, 400, 52)
    pygame.draw.rect(app.pantalla, cfg.COLOR_PANEL, caja, border_radius=10)
    pygame.draw.rect(app.pantalla, cfg.COLOR_ACENTO, caja, width=2, border_radius=10)
    cursor = "|" if pygame.time.get_ticks() // 500 % 2 == 0 else ""
    texto(app.pantalla, app.entrada_nombre + cursor, app.fuente_md, cfg.COLOR_TEXTO,
          centro=caja.center)
    texto(app.pantalla, "Enter para guardar", app.fuente_sm, cfg.COLOR_TEXTO_TENUE,
          centro=(centro_x, 388))

    _dibujar_nombres_existentes(app, centro_x)


def _dibujar_nombres_existentes(app, centro_x: int) -> None:
    nombres = _nombres_existentes(app)
    if not nombres:
        return
    texto(app.pantalla, "o elige uno ya usado:", app.fuente_sm,
          cfg.COLOR_TEXTO_TENUE, centro=(centro_x, 440))
    for rect, nombre in _rects_nombres(nombres):
        pygame.draw.rect(app.pantalla, cfg.COLOR_PANEL, rect, border_radius=8)
        pygame.draw.rect(app.pantalla, cfg.COLOR_ACENTO, rect, width=1, border_radius=8)
        texto(app.pantalla, nombre, app.fuente_sm, cfg.COLOR_TEXTO,
              centro=rect.center)
