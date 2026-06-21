# Juego de Memoria (busqueda de pares)

Juego de memoria en **Python + Pygame**, desarrollado para la asignatura
*Fundamentos de Programacion*. El jugador destapa cartas de dos en dos buscando
formar parejas; gana al emparejarlas todas. Se registran las puntuaciones
(nombre, movimientos y tiempo) en un archivo y se muestra un Top 5 historico.

## Caracteristicas

- Tablero bidimensional (matriz) con dificultades **4x4**, **4x6** y **6x6**.
- Interfaz grafica: menu, tablero clicable y pantalla de puntuaciones.
- Control de turnos con validacion (no repetir carta, no salir de los limites).
- Medicion del desempeno por **movimientos** y **tiempo**.
- Persistencia en `puntuaciones.json` (se actualiza automaticamente al ganar).
- Imagenes propias para las cartas (con respaldo automatico si faltan).
- Efectos de sonido (voltear, acierto, fallo y victoria); si no hay audio,
  el juego sigue funcionando en silencio.

## Estructura

```
src/juego_memoria/
  modelos.py          Carta y resultados de turno
  tablero.py          Matriz de cartas y generacion de parejas
  partida.py          Logica de turnos, movimientos y tiempo (sin Pygame)
  puntuaciones.py     Lectura/escritura de puntuaciones y Top 5
  configuracion.py    Constantes (tamanos, colores, dificultades)
  recursos.py         Carga de imagenes con respaldo
  sonidos.py          Efectos de sonido (tolerante a falta de audio)
  interfaz/           Interfaz Pygame dividida por pantallas
    aplicacion.py       Bucle principal y cambio de pantalla
    disposicion.py      Geometria del tablero (tamano/posicion de cartas)
    dibujo.py           Utilidad para dibujar texto
    estados.py          Nombres de las pantallas
    pantalla_menu.py    Menu de inicio
    pantalla_juego.py   Tablero y marcador
    pantalla_victoria.py    Resultado y registro del ganador
    pantalla_puntuaciones.py  Tabla Top 5
  __main__.py         Punto de entrada
  recursos/imagenes/  <- coloca aqui tus imagenes (ver README de la carpeta)
tests/                Pruebas con pytest de la logica
```

La **logica del juego** (`tablero`, `partida`, `puntuaciones`) no depende de
Pygame, por lo que se prueba con tests automaticos sin abrir ninguna ventana.
Ningun archivo supera las 150 lineas.

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

Desde la raiz del proyecto, en PowerShell, cualquiera de estas opciones:

```powershell
python main.py                       # archivo principal (se relanza solo con el .venv)
.venv\Scripts\python.exe -m juego_memoria
.\jugar.bat                          # lanzador (tambien sirve con doble clic)
```

`main.py` detecta si falta Pygame y se vuelve a ejecutar automaticamente con el
Python del entorno virtual, asi que funciona aunque uses el `python` global.

- **Flechas**: cambiar dificultad · **Enter**: jugar · **P**: ver puntuaciones · **Esc**: salir.
- En la partida, haz **clic** en una carta para destaparla (o en **Menu** para cancelar).

## Desarrollo

```bash
pytest                  # Ejecutar tests
ruff check src tests    # Linter
ruff format src tests   # Formateo
```

## Imagenes de las cartas

Coloca tus imagenes en `src/juego_memoria/recursos/imagenes/` (una por pareja).
Detalles en el README de esa carpeta. Si esta vacia, el juego usa cartas de
color numeradas como respaldo.
