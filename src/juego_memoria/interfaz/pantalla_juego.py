"""Pantalla de juego: tablero clicable, marcador y dibujo de cartas."""

from __future__ import annotations

import pygame

from .. import configuracion as cfg
from ..modelos import ResultadoTurno
from . import disposicion, estados
from .dibujo import texto


def _rect_menu() -> pygame.Rect:
    """Boton para cancelar la partida y volver al menu."""
    return pygame.Rect(cfg.ANCHO_VENTANA - 150, 24, 120, 46)


def eventos(app, evento: pygame.event.Event) -> None:
    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
        app.estado = estados.MENU
    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if app.partida is None:
            return
        # Cancelar la partida y volver al menu.
        if _rect_menu().collidepoint(evento.pos):
            app.estado = estados.MENU
            return
        if app.partida.esperando_desajuste:
            return
        celda = disposicion.celda_en_pixel(app, evento.pos)
        if celda is None:
            return
        fila, columna = celda
        resultado = app.partida.seleccionar(fila, columna)
        if resultado == ResultadoTurno.PRIMERA:
            app.sonidos.reproducir("voltear")
        elif resultado == ResultadoTurno.DESAJUSTE:
            app.sonidos.reproducir("fallo")
            app.desajuste_en = pygame.time.get_ticks()
        elif resultado == ResultadoTurno.PAREJA:
            if app.partida.ganada:
                app.sonidos.reproducir("victoria")
                app.entrada_nombre = ""
                app.estado = estados.VICTORIA
            else:
                app.sonidos.reproducir("acierto")


def dibujar(app) -> None:
    if app.partida is None:
        return
    _dibujar_marcador(app)
    for fila in range(app.partida.tablero.filas):
        for columna in range(app.partida.tablero.columnas):
            _dibujar_carta(app, fila, columna)


def _dibujar_marcador(app) -> None:
    partida = app.partida
    emparejadas = sum(1 for c in partida.tablero.cartas() if c.emparejada) // 2
    texto(app.pantalla, f"Movimientos: {partida.movimientos}", app.fuente_md,
          cfg.COLOR_TEXTO, sup_izq=(30, 22))
    texto(app.pantalla, f"Parejas: {emparejadas}/{partida.tablero.num_parejas}",
          app.fuente_md, cfg.COLOR_TEXTO, sup_izq=(30, 58))
    segundos = int(partida.segundos_transcurridos())
    texto(app.pantalla, f"Tiempo: {segundos // 60:02d}:{segundos % 60:02d}",
          app.fuente_md, cfg.COLOR_TEXTO, centro=(cfg.ANCHO_VENTANA // 2, 45))

    boton = _rect_menu()
    pygame.draw.rect(app.pantalla, cfg.COLOR_PANEL, boton, border_radius=8)
    pygame.draw.rect(app.pantalla, cfg.COLOR_ACENTO, boton, width=2, border_radius=8)
    texto(app.pantalla, "Menu (Esc)", app.fuente_sm, cfg.COLOR_TEXTO,
          centro=boton.center)


def _dibujar_carta(app, fila: int, columna: int) -> None:
    carta = app.partida.tablero.carta_en(fila, columna)
    rect = disposicion.rect_carta(app, fila, columna)
    if carta.boca_arriba:
        app.pantalla.blit(app.imagenes[carta.id_pareja], rect.topleft)
        borde = cfg.COLOR_CARTA_EMPAREJADA if carta.emparejada else cfg.COLOR_RESALTE
        pygame.draw.rect(app.pantalla, borde, rect, width=4, border_radius=8)
    else:
        pygame.draw.rect(app.pantalla, cfg.COLOR_CARTA_DORSO, rect, border_radius=8)
        pygame.draw.rect(app.pantalla, cfg.COLOR_ACENTO, rect, width=2, border_radius=8)
        texto(app.pantalla, "?", app.fuente_lg, cfg.COLOR_CARTA_FRENTE,
              centro=rect.center)
