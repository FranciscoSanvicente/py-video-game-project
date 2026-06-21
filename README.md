# Juego de Memoria (busqueda de pares)

Juego de memoria en **Python + Pygame**, desarrollado para la asignatura
*Fundamentos de Programacion*. El jugador destapa cartas de dos en dos buscando
formar parejas; gana al emparejarlas todas. Se registran los records (nombre,
movimientos y tiempo) en un archivo y se muestra un Top 5 historico.

## Caracteristicas

- Tablero bidimensional (matriz) con dificultades **4x4**, **4x6** y **6x6**.
- Interfaz grafica: menu, tablero clicable y pantalla de records.
- Control de turnos con validacion (no repetir carta, no salir de los limites).
- Medicion de desempeno por **movimientos** y **tiempo**.
- Persistencia de records en `scores.json` (se actualiza automaticamente al ganar).
- Imagenes propias para las cartas (con respaldo automatico si faltan).

## Estructura

```
src/memory_game/
  board.py     Matriz de cartas y generacion de parejas
  game.py      Logica de turnos, movimientos y tiempo (sin Pygame)
  scores.py    Lectura/escritura de records y Top 5
  models.py    Card y resultados de turno
  config.py    Constantes (tamanos, colores, dificultades)
  assets.py    Carga de imagenes con respaldo
  ui.py        Interfaz Pygame (menu, juego, records)
  __main__.py  Punto de entrada
  assets/images/   <- coloca aqui tus imagenes (ver README de la carpeta)
tests/         Pruebas con pytest de la logica
```

La **logica del juego** (`board`, `game`, `scores`) no depende de Pygame, por
lo que se prueba con tests automaticos sin abrir ninguna ventana.

## Instalacion

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

pip install -e ".[dev]"
```

## Como jugar

```bash
python -m memory_game
```

- **Flechas**: cambiar dificultad · **Enter**: jugar · **P**: ver puntuaciones · **Esc**: salir.
- En la partida, haz **clic** en una carta para destaparla.

## Desarrollo

```bash
pytest            # Ejecutar tests
ruff check src tests   # Linter
ruff format src tests  # Formateo
```

## Imagenes de las cartas

Coloca tus imagenes en `src/memory_game/assets/images/` (una por pareja).
Detalles en el README de esa carpeta. Si esta vacia, el juego usa cartas de
color numeradas como respaldo.
