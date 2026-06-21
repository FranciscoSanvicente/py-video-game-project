"""Efectos de sonido del juego.

Carga los archivos WAV de ``recursos/sonidos`` y los reproduce. Si el sistema
no tiene audio disponible (o el mezclador de Pygame falla), el juego sigue
funcionando en silencio: nunca lanza una excepcion por culpa del sonido.
"""

from __future__ import annotations

import pygame

from .configuracion import DIRECTORIO_SONIDOS

# Nombres de los efectos (deben coincidir con los archivos .wav).
EFECTOS = ("voltear", "acierto", "fallo", "victoria")


class Sonidos:
    """Coleccion de efectos de sonido lista para reproducir."""

    def __init__(self) -> None:
        self.activos = False
        self._efectos: dict[str, pygame.mixer.Sound] = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            for nombre in EFECTOS:
                ruta = DIRECTORIO_SONIDOS / f"{nombre}.wav"
                if ruta.exists():
                    self._efectos[nombre] = pygame.mixer.Sound(str(ruta))
            self.activos = bool(self._efectos)
        except pygame.error:
            # Sin tarjeta de sonido o mezclador no disponible: jugar en silencio.
            self.activos = False

    def reproducir(self, nombre: str) -> None:
        """Reproduce el efecto ``nombre`` si esta disponible."""
        efecto = self._efectos.get(nombre)
        if efecto is not None:
            efecto.play()
