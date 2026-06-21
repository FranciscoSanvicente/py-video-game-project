"""Tests de la tabla de puntuaciones (persistencia y ordenamiento)."""

from __future__ import annotations

from juego_memoria.puntuaciones import Puntuacion, TablaPuntuaciones


def _puntuacion(nombre: str, movimientos: int, segundos: float) -> Puntuacion:
    return Puntuacion(nombre=nombre, movimientos=movimientos, segundos=segundos,
                      dificultad="Facil (4x4)", fecha="2026-01-01 10:00")


def test_guarda_y_recarga(tmp_path) -> None:
    archivo = tmp_path / "puntuaciones.json"
    tabla = TablaPuntuaciones(archivo)
    tabla.agregar(_puntuacion("Ana", 10, 45.0))
    # Una nueva instancia debe leer lo guardado en disco.
    recargada = TablaPuntuaciones(archivo)
    assert len(recargada.puntuaciones) == 1
    assert recargada.puntuaciones[0].nombre == "Ana"


def test_orden_por_movimientos_luego_tiempo(tmp_path) -> None:
    tabla = TablaPuntuaciones(tmp_path / "p.json")
    tabla.agregar(_puntuacion("Lento", 10, 100.0))
    tabla.agregar(_puntuacion("Rapido", 5, 80.0))
    tabla.agregar(_puntuacion("Empate", 5, 50.0))
    mejores = tabla.mejores(5)
    assert [p.nombre for p in mejores] == ["Empate", "Rapido", "Lento"]


def test_mejores_limita_resultados(tmp_path) -> None:
    tabla = TablaPuntuaciones(tmp_path / "p.json")
    for i in range(8):
        tabla.agregar(_puntuacion(f"J{i}", i + 1, 10.0))
    assert len(tabla.mejores(5)) == 5


def test_es_record(tmp_path) -> None:
    tabla = TablaPuntuaciones(tmp_path / "p.json")
    for i in range(5):
        tabla.agregar(_puntuacion(f"J{i}", 10 + i, 10.0))  # 10..14 movimientos
    assert tabla.es_record(8, 10.0)        # Mejor que el peor (14).
    assert not tabla.es_record(20, 5.0)    # Peor que todos.


def test_archivo_corrupto_no_rompe(tmp_path) -> None:
    archivo = tmp_path / "p.json"
    archivo.write_text("esto no es json valido {", encoding="utf-8")
    tabla = TablaPuntuaciones(archivo)  # No debe lanzar excepcion.
    assert tabla.puntuaciones == []
