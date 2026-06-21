"""Aplicacion principal: gestiona pantallas, eventos y dibujo.

La logica del juego vive en :class:`~juego_memoria.partida.Partida`; aqui solo
se coordina la ventana y se delega cada pantalla a su modulo correspondiente.
"""

from __future__ import annotations

import pygame

from .. import configuracion as cfg
from ..partida import Partida
from ..puntuaciones import TablaPuntuaciones
from ..recursos import cargar_imagenes_parejas
from . import (
    disposicion,
    estados,
    pantalla_juego,
    pantalla_menu,
    pantalla_puntuaciones,
    pantalla_victoria,
)


class Aplicacion:
    """Coordina el bucle principal y el cambio entre pantallas."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(cfg.TITULO)
        self.pantalla = pygame.display.set_mode((cfg.ANCHO_VENTANA, cfg.ALTO_VENTANA))
        self.reloj = pygame.time.Clock()
        self.ejecutando = True

        # Fuentes reutilizables.
        self.fuente_xl = pygame.font.SysFont("arial", 56, bold=True)
        self.fuente_lg = pygame.font.SysFont("arial", 34, bold=True)
        self.fuente_md = pygame.font.SysFont("arial", 26)
        self.fuente_sm = pygame.font.SysFont("arial", 20)

        self.tabla = TablaPuntuaciones()
        self.estado = estados.MENU
        self.dificultad = cfg.DIFICULTAD_PREDETERMINADA

        # Estado de partida (se crea al iniciar una nueva).
        self.partida: Partida | None = None
        self.imagenes: dict[int, pygame.Surface] = {}
        self.tamano_carta = 0
        self.origen = (0, 0)
        self.separacion = 12
        self.desajuste_en: int | None = None   # Momento del desajuste (ticks).
        self.entrada_nombre = ""               # Nombre del ganador en pantalla.

    def ejecutar(self) -> None:
        """Bucle de juego: eventos -> actualizacion -> dibujo, a ``FPS``."""
        while self.ejecutando:
            self._manejar_eventos()
            self._actualizar()
            self._dibujar()
            self.reloj.tick(cfg.FPS)
        pygame.quit()

    def iniciar_partida(self) -> None:
        """Crea una nueva partida con la dificultad seleccionada."""
        filas, columnas = cfg.DIFICULTADES[self.dificultad]
        self.partida = Partida(filas, columnas)
        self.desajuste_en = None
        disposicion.calcular_disposicion(self, filas, columnas)
        self.imagenes = cargar_imagenes_parejas(
            self.partida.tablero.num_parejas, self.tamano_carta
        )
        self.estado = estados.JUGANDO

    def _manejar_eventos(self) -> None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            elif self.estado == estados.MENU:
                pantalla_menu.eventos(self, evento)
            elif self.estado == estados.JUGANDO:
                pantalla_juego.eventos(self, evento)
            elif self.estado == estados.VICTORIA:
                pantalla_victoria.eventos(self, evento)
            elif self.estado == estados.PUNTUACIONES:
                pantalla_puntuaciones.eventos(self, evento)

    def _actualizar(self) -> None:
        """Oculta las cartas no coincidentes tras la pausa configurada."""
        if self.estado == estados.JUGANDO and self.desajuste_en is not None:
            assert self.partida is not None
            if pygame.time.get_ticks() - self.desajuste_en >= cfg.RETARDO_DESAJUSTE_MS:
                self.partida.resolver_desajuste()
                self.desajuste_en = None

    def _dibujar(self) -> None:
        self.pantalla.fill(cfg.COLOR_FONDO)
        if self.estado == estados.MENU:
            pantalla_menu.dibujar(self)
        elif self.estado == estados.JUGANDO:
            pantalla_juego.dibujar(self)
        elif self.estado == estados.VICTORIA:
            pantalla_juego.dibujar(self)       # Tablero resuelto de fondo.
            pantalla_victoria.dibujar(self)
        elif self.estado == estados.PUNTUACIONES:
            pantalla_puntuaciones.dibujar(self)
        pygame.display.flip()
