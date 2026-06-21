"""Genera los efectos de sonido del juego como archivos WAV.

Usa solo la libreria estandar (``wave``, ``struct``, ``math``), sintetizando
ondas senoidales con una envolvente simple para evitar chasquidos. Asi el
proyecto no depende de archivos de sonido externos.

Ejecutar (desde la raiz del proyecto):

    .venv\\Scripts\\python.exe scripts\\generar_sonidos.py
"""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

FRECUENCIA_MUESTREO = 44100
DESTINO = (
    Path(__file__).resolve().parent.parent
    / "src" / "juego_memoria" / "recursos" / "sonidos"
)


def _onda(notas: list[float], duracion: float, volumen: float = 0.5) -> list[float]:
    """Genera las muestras de una secuencia de ``notas`` (en Hz) de igual duracion."""
    total = int(FRECUENCIA_MUESTREO * duracion)
    por_nota = max(1, total // len(notas))
    ataque = int(0.01 * FRECUENCIA_MUESTREO)
    muestras: list[float] = []
    for frecuencia in notas:
        for i in range(por_nota):
            tiempo = i / FRECUENCIA_MUESTREO
            subida = min(1.0, i / ataque)
            bajada = max(0.0, 1.0 - i / por_nota)
            envolvente = subida * bajada
            muestras.append(volumen * envolvente * math.sin(2 * math.pi * frecuencia * tiempo))
    return muestras


def _guardar(nombre: str, muestras: list[float]) -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    ruta = DESTINO / f"{nombre}.wav"
    with wave.open(str(ruta), "w") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(FRECUENCIA_MUESTREO)
        datos = b"".join(
            struct.pack("<h", int(max(-1.0, min(1.0, m)) * 32767)) for m in muestras
        )
        archivo.writeframes(datos)
    print(f"  {ruta.name}")


def main() -> None:
    print("Generando sonidos en", DESTINO)
    _guardar("voltear", _onda([700.0], 0.08, 0.40))
    _guardar("acierto", _onda([660.0, 990.0], 0.18, 0.50))
    _guardar("fallo", _onda([320.0, 200.0], 0.22, 0.45))
    _guardar("victoria", _onda([523.0, 659.0, 784.0, 1046.0], 0.5, 0.50))


if __name__ == "__main__":
    main()
