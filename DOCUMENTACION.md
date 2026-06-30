# 📖 Documentación del Juego de Memoria — explicada desde cero

> Este documento está escrito para una persona que **nunca ha programado** y no
> conoce Python. Vamos a explicar todo poco a poco, con ejemplos de la vida real,
> como si se lo contáramos a un niño. No necesitas saber nada previo. 🙂

---

## Índice

1. [¿Qué es este proyecto?](#1-qué-es-este-proyecto)
2. [Ideas básicas de programación (para entender todo lo demás)](#2-ideas-básicas-de-programación)
3. [Los "estilos" de programar que usamos (paradigmas)](#3-los-paradigmas-que-usamos)
4. [¿Cómo funciona el juego por dentro? (la idea general)](#4-cómo-funciona-el-juego-por-dentro)
5. [Mapa de archivos: qué hace cada uno](#5-mapa-de-archivos)
6. [Explicación archivo por archivo](#6-explicación-archivo-por-archivo)
7. [Glosario rápido](#7-glosario-rápido)

---

## 1. ¿Qué es este proyecto?

Es un **juego de memoria** (el clásico de buscar parejas de cartas). Ves un
tablero con cartas boca abajo, volteas dos, y si son iguales se quedan; si no,
se vuelven a ocultar. Ganas cuando emparejas todas.

El juego está hecho con **Python** (un lenguaje de programación) y una
herramienta llamada **Pygame**, que sirve para dibujar en pantalla, detectar
clics del ratón y reproducir sonidos.

---

## 2. Ideas básicas de programación

Antes de mirar el código, necesitas entender unas pocas palabras. Usaremos
analogías de la vida real.

### 🧾 Un programa es como una receta de cocina
Un programa es una **lista de instrucciones** que la computadora sigue paso a
paso, igual que tú sigues una receta: "primero esto, luego esto otro".

### 📦 Variable = una caja con etiqueta
Una **variable** es una caja donde guardas un dato y le pones un nombre.
```python
movimientos = 0      # una caja llamada "movimientos" que guarda el número 0
nombre = "Ana"       # una caja llamada "nombre" que guarda la palabra "Ana"
```
Si más adelante escribes `movimientos = 5`, cambias lo que hay dentro de la caja.

### 🔀 Tipos de datos (qué clase de cosa hay en la caja)
- **Número entero** (`int`): `0`, `5`, `42`.
- **Número con decimales** (`float`): `3.5`, `93.2`.
- **Texto** (`str`): `"Ana"`, `"Juego de Memoria"`. Siempre entre comillas.
- **Interruptor** (`bool`): solo dos valores, `True` (verdadero) o `False`
  (falso). Como un foco: encendido o apagado.

### 📋 Lista = una fila de casilleros numerados
Una **lista** guarda varias cosas en orden.
```python
colores = ["rojo", "verde", "azul"]
```
El primer casillero es el número `0` (en programación se empieza a contar
desde 0): `colores[0]` es `"rojo"`.

### 📒 Diccionario = una agenda de contactos
Un **diccionario** guarda parejas de "nombre → valor", como una agenda donde
buscas por nombre y obtienes el teléfono.
```python
dificultades = {"Facil": (4, 4), "Dificil": (6, 6)}
dificultades["Facil"]   # te da (4, 4)
```

### ⚙️ Función = una maquinita que hace un trabajo
Una **función** es un conjunto de instrucciones con un nombre. Le das algo
(entrada), hace su trabajo y a veces te devuelve un resultado (salida). Como
una licuadora: metes fruta, sale jugo.
```python
def sumar(a, b):        # "def" significa "definir una función"
    return a + b        # "return" = devolver el resultado
sumar(2, 3)             # esto vale 5
```
- Lo que va entre paréntesis (`a`, `b`) son los **parámetros** (lo que recibe).
- `return` entrega el resultado a quien llamó la función.

### 🤔 Decisiones (`if`) = "si pasa esto, haz aquello"
```python
if movimientos == 0:
    print("Aún no jugaste")
else:
    print("Ya hiciste tu primer movimiento")
```

### 🔁 Repeticiones (`for`) = "haz esto para cada cosa"
```python
for color in colores:
    print(color)        # imprime rojo, luego verde, luego azul
```

### 🏗️ Clase = un molde / plano. Objeto = lo que sale del molde
Una **clase** es como el plano de una casa o el molde de una galleta. Con un
mismo molde puedes hacer muchas galletas. Cada galleta es un **objeto**.

- Una clase `Carta` es el molde de "cómo es una carta".
- Cada carta concreta del tablero es un **objeto** hecho con ese molde.

Dentro de una clase hay:
- **Atributos**: los datos del objeto (sus características). Ej.: una carta
  tiene `fila`, `columna`, y si está `revelada`.
- **Métodos**: las acciones que el objeto sabe hacer (son funciones que viven
  dentro de la clase). Ej.: un tablero sabe decir si `todas_emparejadas()`.

### 🪄 La palabra `self`
Dentro de una clase verás mucho `self`. Significa **"yo mismo"**: se refiere al
objeto concreto con el que estás trabajando. Cuando una carta dice
`self.revelada = True`, significa "*mi* atributo revelada ahora es verdadero".

### 🧰 Librería / módulo = una caja de herramientas ya hecha
En vez de inventar todo, usamos herramientas que otros ya construyeron. Eso es
una **librería**. Aquí usamos **Pygame** (para ventana, dibujo, ratón y sonido).
`import pygame` significa "tráeme esa caja de herramientas".

---

## 3. Los paradigmas que usamos

Un **paradigma** es un "estilo" o forma de organizar el código. Este proyecto
mezcla varios (es muy común combinarlos):

### a) Programación estructurada
Es lo más básico: el programa avanza con **secuencias** (un paso tras otro),
**decisiones** (`if`) y **repeticiones** (`for`). Está presente en todo el
código.

### b) Programación Orientada a Objetos (POO) 🎯
La idea estrella del proyecto: representamos las cosas del juego como
**objetos** con sus datos y sus acciones. Tenemos clases como `Carta`,
`Tablero`, `Partida`, `Aplicacion`. Cada una se encarga de "su mundo".

> **Analogía:** en una obra de teatro, cada actor (objeto) sabe su papel. El
> director (la `Aplicacion`) coordina, pero no actúa por ellos.

### c) Separación de responsabilidades (lógica vs. interfaz) 🧠🎨
Dividimos el juego en dos mundos:
- **El cerebro (la lógica):** las reglas del juego — `tablero.py`, `partida.py`,
  `puntuaciones.py`. **No sabe dibujar ni nada de Pygame.**
- **La cara (la interfaz):** lo que ves y tocas — la carpeta `interfaz/`.

> **¿Por qué?** Porque así podemos **probar el cerebro** con tests automáticos
> sin abrir ninguna ventana, y si algún día cambiamos los dibujos, el cerebro
> sigue intacto. Es como separar el motor de un coche de su carrocería.

### d) Máquina de estados (las pantallas) 🚦
El juego siempre está en **una** de cuatro "pantallas": menú, jugando,
victoria o puntuaciones. A eso se le llama **estado**. El programa cambia de un
estado a otro según lo que hagas. Es como un semáforo que está en rojo, amarillo
o verde, nunca en dos a la vez.

### e) Programación dirigida por eventos 🖱️
El juego espera a que **ocurran cosas** (eventos): que muevas el ratón, hagas
clic, presiones una tecla, o cierres la ventana. Cada evento dispara una
reacción. A esto se le llama "bucle de eventos".

---

## 4. ¿Cómo funciona el juego por dentro?

Todos los videojuegos funcionan con un **bucle principal** (en inglés, *game
loop*): una repetición que ocurre muchísimas veces por segundo (aquí, **60
veces por segundo**). En cada vuelta hace 3 cosas:

```
   ┌─────────────────────────────────────────────┐
   │   1) MIRAR  → ¿qué hizo el jugador?          │  (eventos: clic, tecla…)
   │   2) PENSAR → actualizar el estado del juego │  (¿toca ocultar cartas?)
   │   3) PINTAR → dibujar todo en la pantalla    │  (menú, tablero, etc.)
   └─────────────────────────────────────────────┘
              ↑__________ se repite 60 veces/seg __________↓
```

Como se repite tan rápido, nuestros ojos ven movimiento fluido, igual que un
dibujo animado son muchas imágenes seguidas.

**Recorrido típico de una partida:**
1. Arranca en la pantalla **menú**.
2. Eliges dificultad y pulsas Jugar → pasa a **jugando** y crea el tablero.
3. Haces clic en cartas. La lógica decide si hay pareja o no.
4. Cuando emparejas todo → pasa a **victoria**, escribes tu nombre.
5. Se guarda tu puntuación → pasa a **puntuaciones** (el Top 5).
6. Vuelves al **menú**.

---

## 5. Mapa de archivos

El código está separado en "el cerebro" y "la cara":

```
src/juego_memoria/
│
├── 🧠 EL CEREBRO (reglas del juego, sin dibujos)
│   ├── modelos.py        Define qué es una "Carta" y los resultados de un turno
│   ├── tablero.py        El tablero: la cuadrícula de cartas y sus parejas
│   ├── partida.py        Las reglas: turnos, validar jugadas, contar tiempo
│   └── puntuaciones.py   Guardar y leer los récords en un archivo
│
├── 🔧 APOYO
│   ├── configuracion.py  Todos los "ajustes": tamaños, colores, dificultades
│   ├── recursos.py       Carga las imágenes de las cartas
│   └── sonidos.py        Carga y reproduce los efectos de sonido
│
├── 🎨 LA CARA (lo que ves y tocas)
│   └── interfaz/
│       ├── aplicacion.py          El "director": el bucle principal
│       ├── estados.py             Los nombres de las 4 pantallas
│       ├── disposicion.py         Calcula dónde va cada carta en la pantalla
│       ├── dibujo.py              Ayuda a escribir texto en pantalla
│       ├── pantalla_menu.py       Dibuja y maneja el menú
│       ├── pantalla_juego.py      Dibuja y maneja el tablero
│       ├── pantalla_victoria.py   Pide el nombre del ganador
│       └── pantalla_puntuaciones.py  Muestra el Top 5
│
├── __main__.py    Permite arrancar con "python -m juego_memoria"
└── recursos/      Carpetas con las imágenes y los sonidos

main.py            Arranca el juego desde la consola (en la raíz del proyecto)
```

> **Idea clave:** cada archivo tiene **un solo trabajo**. Es más fácil entender
> y arreglar 17 archivos pequeños que un archivo gigante.

---

## 6. Explicación archivo por archivo

En cada archivo verás líneas como `from __future__ import annotations` y
`"""texto"""` al inicio. Vamos a explicar esas dos primero, porque se repiten
en casi todos:

- **`"""texto entre triples comillas"""`**: es un **comentario de
  documentación** (un *docstring*). No hace nada al ejecutarse; solo explica,
  para los humanos, qué hace ese archivo, clase o función. *Si se quitara, el
  programa funcionaría igual, pero nadie entendería el código.*
- **`from __future__ import annotations`**: un detalle técnico que permite
  escribir las "pistas de tipo" (como `int`, `str`) de forma más cómoda y
  moderna. *Si se quitara, en algunos casos Python se quejaría; es una buena
  práctica tenerlo.*
- **`# comentario con almohadilla`**: nota para humanos en una sola línea.
  Python la ignora.

---

### 🧠 `modelos.py` — las piezas más básicas

Define dos cosas: qué puede pasar en un turno, y qué es una carta.

```python
class ResultadoTurno(Enum):
    PRIMERA = "primera"
    PAREJA = "pareja"
    DESAJUSTE = "desajuste"
    INVALIDO = "invalido"
```
- Un **`Enum`** (enumeración) es una **lista de opciones con nombre**, como las
  caras de un dado o los colores de un semáforo. Aquí dice: "el resultado de
  tocar una carta solo puede ser una de estas 4 cosas".
- ¿Por qué usar esto en vez de texto suelto? Porque evita errores de
  escritura: si escribieras `"pareya"` por error, el programa no avisaría; pero
  `ResultadoTurno.PAREJA` está garantizado.

```python
@dataclass
class Carta:
    id_pareja: int
    fila: int
    columna: int
    revelada: bool = False
    emparejada: bool = False
```
- `class Carta` es el **molde de una carta**.
- **`@dataclass`** es un "ayudante" mágico de Python: escribe por nosotros el
  código aburrido para crear una carta con sus datos. *Si se quitara,
  tendríamos que escribir mucho más código a mano para lo mismo.*
- Los **atributos** (datos de cada carta):
  - `id_pareja`: el número de su pareja. Dos cartas con el mismo `id_pareja`
    son la pareja que hay que encontrar.
  - `fila`, `columna`: en qué casillero del tablero está.
  - `revelada = False`: ¿está boca arriba ahora mismo? Empieza en `False`
    (boca abajo). El `= False` es el **valor por defecto**.
  - `emparejada = False`: ¿ya se encontró su pareja? Empieza en `False`.

```python
    @property
    def boca_arriba(self) -> bool:
        return self.revelada or self.emparejada
```
- Un **método** que responde una pregunta: "¿se ve la cara de esta carta?".
- La carta se ve si está `revelada` (la acabas de voltear) **o** si ya está
  `emparejada` (se quedó descubierta). El `or` significa "cualquiera de las dos".
- **`@property`** hace que se use como si fuera un dato (`carta.boca_arriba`) en
  lugar de una función con paréntesis. Es solo comodidad de lectura.

---

### 🧠 `tablero.py` — la cuadrícula de cartas

Aquí vive la clase `Tablero`, que representa la **matriz** (cuadrícula) de
cartas. Una matriz es una tabla de filas y columnas, como un tablero de ajedrez
o una hoja de Excel.

```python
def __init__(self, filas, columnas, *, semilla=None):
    if (filas * columnas) % 2 != 0:
        raise ValueError("...debe ser par.")
    self.filas = filas
    self.columnas = columnas
    self.matriz = self._construir_matriz(random.Random(semilla))
```
- **`__init__`** es un método especial llamado **"constructor"**: se ejecuta
  automáticamente cuando se crea un tablero nuevo. Es el "nacimiento" del objeto.
- `if (filas * columnas) % 2 != 0:` comprueba que el número de casillas sea
  **par**. El símbolo `%` da el **residuo** de una división; `% 2` te dice si un
  número es par (residuo 0) o impar (residuo 1). *Si faltara esta comprobación,
  podrías crear un tablero con una carta sin pareja, y el juego nunca podría
  terminarse.*
- `raise ValueError(...)` **lanza un error** a propósito para frenar el problema
  de inmediato con un mensaje claro.
- `self.filas = filas` guarda el dato dentro del objeto para usarlo después.
- `semilla` sirve para barajar siempre igual cuando hacemos pruebas (para que el
  resultado sea predecible). En el juego normal no se usa, así que las cartas
  salen al azar.

```python
def _construir_matriz(self, generador):
    identificadores = [pareja for pareja in range(self.num_parejas) for _ in range(2)]
    generador.shuffle(identificadores)
    ...
```
- Crea la cuadrícula. Primero arma una lista con **cada número de pareja
  repetido dos veces** (`0,0,1,1,2,2,...`): así garantizamos que cada carta
  tenga exactamente una pareja.
- `generador.shuffle(...)` **baraja** esa lista, como mezclar un mazo.
- Luego recorre fila por fila y columna por columna creando las `Carta` y
  colocándolas. El resultado es una **lista de listas** (filas que contienen
  cartas): por eso se accede como `matriz[fila][columna]`.
- El guion bajo inicial en `_construir_matriz` es una **convención**: significa
  "esto es de uso interno, no lo llames desde fuera".

Los demás métodos son preguntas/acciones sobre el tablero:
- `num_parejas`: cuántas parejas hay (la mitad de las casillas).
- `dentro_limites(fila, columna)`: ¿esa posición existe en el tablero? Evita
  buscar en un casillero que no existe. *Sin esto, el juego podría reventar al
  hacer clic fuera de la cuadrícula.*
- `carta_en(fila, columna)`: te entrega la carta de esa casilla.
- `cartas()`: te da **todas** las cartas en una sola fila (lista plana), cómodo
  para recorrerlas.
- `todas_emparejadas()`: devuelve `True` si **todas** las cartas ya están
  emparejadas. Así sabemos que el jugador ganó. La función `all(...)` significa
  "¿se cumple para todas?".

---

### 🧠 `partida.py` — las reglas del juego

La clase `Partida` es el **árbitro**: recibe "el jugador tocó la casilla (fila,
columna)" y decide qué pasa. **No dibuja nada**; solo aplica las reglas.

Atributos importantes que guarda (en `__init__`):
- `self.tablero`: el tablero de esta partida.
- `self.movimientos = 0`: cuántas parejas ha intentado (el marcador).
- `self.primera` / `self.segunda`: las cartas que tienes volteadas ahora.
  Empiezan en `None`, que significa "nada / vacío".
- `self._tiempo_inicio`: el momento exacto en que empezó, para cronometrar.
- `reloj=time.monotonic`: el "reloj" que usa para medir el tiempo. Se puede
  cambiar por uno falso en las pruebas (un truco para testear el tiempo sin
  esperar de verdad).

```python
def segundos_transcurridos(self):
    fin = self._tiempo_fin if self._tiempo_fin is not None else self._reloj()
    return fin - self._tiempo_inicio
```
- Calcula cuántos segundos llevas jugando: tiempo de ahora menos tiempo de
  inicio. Cuando ganas, el cronómetro se **congela** (guarda `_tiempo_fin`) para
  que el récord no siga aumentando.

```python
def seleccionar(self, fila, columna):
    if self.esperando_desajuste or self.ganada:
        return ResultadoTurno.INVALIDO
    if not self.tablero.dentro_limites(fila, columna):
        return ResultadoTurno.INVALIDO
    carta = self.tablero.carta_en(fila, columna)
    if carta.emparejada or carta.revelada:
        return ResultadoTurno.INVALIDO
    carta.revelada = True
    if self.primera is None:
        self.primera = carta
        return ResultadoTurno.PRIMERA
    self.movimientos += 1
    if carta.id_pareja == self.primera.id_pareja:
        self.primera.emparejada = True
        carta.emparejada = True
        self.primera = None
        if self.ganada:
            self._tiempo_fin = self._reloj()
        return ResultadoTurno.PAREJA
    self.segunda = carta
    return ResultadoTurno.DESAJUSTE
```
Este es el **corazón del juego**. Vamos paso a paso, como una historia:
1. **"¿Es buen momento para jugar?"** Si ya hay dos cartas mostrándose esperando
   ocultarse, o ya ganaste, la jugada no vale → `INVALIDO`. *Sin esto, podrías
   voltear una tercera carta y romper la lógica.*
2. **"¿Esa casilla existe?"** Si tocaste fuera del tablero → `INVALIDO`.
3. **"¿Esa carta se puede tocar?"** Si ya está emparejada o ya la volteaste →
   `INVALIDO`. *Sin esto podrías "emparejar" una carta consigo misma.*
4. `carta.revelada = True`: la volteamos boca arriba.
5. **¿Es la primera del turno?** Si no tenías ninguna volteada, esta es la
   primera. La recordamos y devolvemos `PRIMERA`.
6. Si ya había una, esta es la **segunda**: sumamos `+1` al marcador de
   movimientos y comparamos.
7. **¿Son pareja?** (`carta.id_pareja == self.primera.id_pareja`). Si sí, marcamos
   ambas como `emparejada`, limpiamos la "primera", y si ya ganaste, congelamos
   el tiempo → `PAREJA`.
8. **Si no son pareja** → guardamos la segunda y devolvemos `DESAJUSTE`. Las dos
   se quedan visibles un momentito (la interfaz se encarga de la pausa).

```python
def resolver_desajuste(self):
    if self.primera is not None:
        self.primera.revelada = False
    if self.segunda is not None:
        self.segunda.revelada = False
    self.primera = None
    self.segunda = None
```
- Cuando las dos cartas no eran pareja, tras una breve pausa esta función las
  **vuelve a ocultar** y limpia el turno para empezar de nuevo.

---

### 🧠 `puntuaciones.py` — guardar los récords

Aquí se guardan y leen las mejores puntuaciones en un archivo, para que **no se
pierdan al cerrar el juego** (eso se llama *persistencia*).

```python
@dataclass
class Puntuacion:
    nombre: str
    movimientos: int
    segundos: float
    dificultad: str
    fecha: str
    def clave_orden(self):
        return (self.movimientos, self.segundos)
```
- `Puntuacion` es el molde de **un récord**: quién, en cuántos movimientos, en
  cuánto tiempo, en qué dificultad y cuándo.
- `clave_orden` define qué significa "mejor": **menos movimientos primero**, y
  si empatan, **menos tiempo**.

La clase `TablaPuntuaciones` administra todos los récords:
- `__init__`: al crearse, **lee** el archivo de récords con `_cargar()`.
- `_cargar()`: si el archivo no existe o está dañado, devuelve una lista vacía
  en lugar de romperse (el `try/except` "atrapa" el error). *Sin ese
  `try/except`, un archivo corrupto haría fallar todo el juego al abrir.*
- `guardar()`: escribe los récords en el archivo en formato **JSON** (una forma
  estándar de guardar datos como texto, fácil de leer).
- `agregar(puntuacion)`: añade un récord nuevo y guarda enseguida.
- `mejores(limite=5)`: devuelve los **5 mejores** ya ordenados. `sorted(...)`
  ordena, y `[:limite]` toma solo los primeros 5.
- `es_record(...)`: dice si una puntuación entraría en el Top 5.

> **Formato JSON, ejemplo de lo que se guarda:**
> ```json
> [ { "nombre": "Ana", "movimientos": 12, "segundos": 45.0,
>     "dificultad": "Facil (4x4)", "fecha": "2026-06-30 10:00" } ]
> ```

---

### 🔧 `configuracion.py` — el panel de ajustes

No tiene clases ni funciones: solo **constantes** (valores fijos con nombre).
Es como el tablero de mandos del juego. Si quieres cambiar un color o el tamaño
de la ventana, lo haces aquí en un solo sitio.

- `DIRECTORIO_IMAGENES`, `DIRECTORIO_SONIDOS`: dónde están las imágenes y sonidos.
- `ARCHIVO_PUNTUACIONES = "puntuaciones.json"`: nombre del archivo de récords.
- `DIFICULTADES`: un **diccionario** que relaciona cada nombre de dificultad con
  el tamaño del tablero. Ej.: `"Facil (4x4)" → (4, 4)`.
- `ANCHO_VENTANA`, `ALTO_VENTANA`: tamaño de la ventana en píxeles.
- `FPS = 60`: cuántas veces por segundo se repite el bucle (*frames per second*).
- `RETARDO_DESAJUSTE_MS = 800`: cuántos milisegundos se ven las cartas que no
  hicieron pareja antes de ocultarse (800 ms = 0,8 segundos).
- Los `COLOR_...` son colores escritos como `(Rojo, Verde, Azul)`, cada valor de
  0 a 255. Así se mezclan los colores en pantalla.

Hay un detalle especial al inicio:
```python
if getattr(sys, "frozen", False):
    DIRECTORIO_PAQUETE = Path(sys._MEIPASS) / "juego_memoria"
else:
    DIRECTORIO_PAQUETE = Path(__file__).resolve().parent
```
- Esto distingue si el juego corre **normal** o **dentro del .exe** empaquetado
  (cuando se hace un ejecutable, los archivos viven en un sitio temporal
  distinto). Así encuentra las imágenes y sonidos en ambos casos.

---

### 🔧 `recursos.py` — las imágenes de las cartas

Carga las imágenes que el jugador pone en la carpeta `recursos/imagenes`. Lo
inteligente: **si faltan imágenes, las inventa** (cartas de color con un número),
para que el juego funcione siempre.

- `_listar_archivos_imagen()`: busca los archivos de imagen en la carpeta.
- `_crear_respaldo(id_pareja, tamano)`: dibuja una carta de color con un número,
  usada cuando no hay imagen para esa pareja.
- `cargar_imagenes_parejas(num_parejas, tamano)`: arma un **diccionario**
  `id_pareja → imagen`. Para cada pareja: usa la imagen del jugador si existe;
  si no, usa el respaldo. *Sin esta lógica de respaldo, el juego se quedaría sin
  poder dibujar cartas hasta que añadieras fotos a mano.*

---

### 🔧 `sonidos.py` — los efectos de sonido

La clase `Sonidos` carga los 4 efectos (`voltear`, `acierto`, `fallo`,
`victoria`) y los reproduce.

- En `__init__`, todo el cargado va dentro de un `try/except`: si la computadora
  **no tiene audio**, marca `self.activos = False` y el juego sigue **en
  silencio** sin romperse. *Sin ese `try/except`, en una máquina sin tarjeta de
  sonido el juego no abriría.*
- `reproducir(nombre)`: suena el efecto pedido. Si ese efecto no existe,
  simplemente no hace nada (no falla).

---

### 🎨 `interfaz/estados.py` — los nombres de las pantallas

Apenas 4 líneas que dan nombre a las cuatro pantallas:
```python
MENU = "menu"
JUGANDO = "jugando"
VICTORIA = "victoria"
PUNTUACIONES = "puntuaciones"
```
Usar `estados.MENU` en vez de escribir `"menu"` a mano por todo el código evita
errores de tecleo. La "máquina de estados" de la que hablamos en los paradigmas
vive gracias a esto.

---

### 🎨 `interfaz/dibujo.py` — la ayudante para escribir texto

Tiene una sola función, `texto(...)`, que **escribe una frase en la pantalla**.
Dibujar texto con Pygame requiere varios pasos repetitivos; esta función los
junta en uno solo, así no repetimos ese código en cada pantalla.
- Recibe dónde y cómo escribir (la frase, la fuente, el color, la posición).
- Puede colocar el texto por su **centro** o por su **esquina** superior
  izquierda. *Si esta función no existiera, cada pantalla tendría que repetir
  4-5 líneas cada vez que muestra una palabra.*

---

### 🎨 `interfaz/disposicion.py` — dónde va cada carta

Hace las **matemáticas de colocación**: calcula de qué tamaño dibujar las cartas
y en qué posición, para que el tablero quede **centrado** y quepa bien sin
importar si es 4x4 o 6x6.

- `calcular_disposicion(app, filas, columnas)`: decide el tamaño de cada carta
  (el mayor posible que quepa) y el punto de inicio del tablero.
- `rect_carta(app, fila, columna)`: devuelve el **rectángulo** (posición y
  tamaño) de una carta concreta en pantalla.
- `celda_en_pixel(app, posicion)`: hace lo contrario — dado un punto donde
  hiciste clic, averigua **qué carta** está ahí (o `None` si fue en un hueco).
  *Esta es la traducción "clic del ratón → carta del tablero".*

---

### 🎨 `interfaz/aplicacion.py` — el director de orquesta

La clase `Aplicacion` es la **más importante de la interfaz**: arranca todo y
ejecuta el bucle principal. Es el "director" que coordina a los demás.

En `__init__` prepara todo lo necesario una sola vez:
- `pygame.init()`: enciende Pygame. *Sin esto, nada de dibujo/sonido funciona.*
- `set_mode(...)`: crea la **ventana** del tamaño configurado.
- `self.reloj = pygame.time.Clock()`: un reloj para mantener los 60 FPS.
- Carga las **fuentes** de texto (tamaños xl, lg, md, sm).
- Crea la tabla de récords (`self.tabla`) y los sonidos (`self.sonidos`).
- `self.estado = estados.MENU`: el juego empieza en el menú.
- Prepara variables que se usarán al jugar (`partida`, `imagenes`, etc.).

```python
def ejecutar(self):
    while self.ejecutando:
        self._manejar_eventos()
        self._actualizar()
        self._dibujar()
        self.reloj.tick(cfg.FPS)
    pygame.quit()
```
- Este es **el bucle principal** del que hablamos. `while self.ejecutando:`
  significa "repite mientras el juego siga abierto". Las 3 llamadas son MIRAR,
  PENSAR y PINTAR. `tick(60)` frena el ritmo para que sean 60 vueltas por
  segundo (si no, iría descontroladamente rápido). `pygame.quit()` apaga todo al
  cerrar.

```python
def iniciar_partida(self):
    filas, columnas = cfg.DIFICULTADES[self.dificultad]
    self.partida = Partida(filas, columnas)
    ...
    self.estado = estados.JUGANDO
```
- Empieza una partida nueva: mira el tamaño de la dificultad elegida, crea la
  `Partida` (el cerebro), calcula la disposición, carga las imágenes y cambia el
  estado a "jugando".

```python
def _manejar_eventos(self):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            self.ejecutando = False
        elif self.estado == estados.MENU:
            pantalla_menu.eventos(self, evento)
        elif self.estado == estados.JUGANDO:
            pantalla_juego.eventos(self, evento)
        ...
```
- Revisa **todo lo que hizo el jugador** desde la última vuelta. Si cerró la
  ventana (`QUIT`), termina. Si no, le pasa el evento a la pantalla que esté
  activa. Esto es la **máquina de estados** en acción: según el estado, manda el
  evento a un sitio u otro.

```python
def _actualizar(self):
    if self.estado == estados.JUGANDO and self.desajuste_en is not None:
        if pygame.time.get_ticks() - self.desajuste_en >= cfg.RETARDO_DESAJUSTE_MS:
            self.partida.resolver_desajuste()
            self.desajuste_en = None
```
- La parte de **PENSAR**: si dos cartas no coincidieron y ya pasó el tiempito de
  espera (0,8 s), las oculta. Es lo que da ese momento para memorizarlas.

```python
def _dibujar(self):
    self.pantalla.fill(cfg.COLOR_FONDO)
    if self.estado == estados.MENU:
        pantalla_menu.dibujar(self)
    elif self.estado == estados.JUGANDO:
        pantalla_juego.dibujar(self)
    ...
    pygame.display.flip()
```
- La parte de **PINTAR**: primero pinta el fondo (borra lo anterior), luego pide
  a la pantalla activa que se dibuje. `pygame.display.flip()` **muestra** en el
  monitor todo lo que se acaba de dibujar. *Sin `flip()`, dibujarías pero la
  pantalla se quedaría en negro.*

> Fíjate que `Aplicacion` no sabe los detalles de cada pantalla: solo dice "menú,
> dibújate tú". Cada pantalla es experta en lo suyo. Eso es la separación de
> responsabilidades.

---

### 🎨 `interfaz/pantalla_menu.py` — la pantalla de inicio

Cada pantalla tiene dos funciones gemelas: **`eventos(...)`** (qué hacer cuando
el jugador actúa) y **`dibujar(...)`** (cómo se ve).

- Las funciones `_rects_dificultad()`, `_rect_jugar()`, `_rect_puntuaciones()`
  definen los **rectángulos** (zonas) de los botones. Saber dónde está cada
  botón sirve tanto para dibujarlo como para detectar el clic encima.
- `eventos(app, evento)`:
  - Con el **teclado**: flechas para cambiar dificultad, Enter para jugar, `P`
    para ver récords, `Esc` para salir.
  - Con el **ratón**: si haces clic en una dificultad, la selecciona; en "Jugar",
    empieza; en "Puntuaciones", muestra el Top 5.
  - El truco `(i - 1) % len(nombres)` hace que al pasar del primero hacia atrás,
    saltes al último (una rueda que da la vuelta).
- `dibujar(app)`: pinta el título, las tres dificultades (resaltando la elegida)
  y los botones, usando la función `texto` y rectángulos de colores.

---

### 🎨 `interfaz/pantalla_juego.py` — el tablero

La pantalla donde realmente juegas.

- `_rect_menu()`: la zona del botón "Menu (Esc)" para cancelar la partida.
- `eventos(app, evento)`:
  - `Esc` o clic en el botón "Menu" → vuelve al menú (cancela la partida).
  - Si hiciste clic en una carta, traduce el clic a una casilla (con
    `celda_en_pixel`) y se la pasa al cerebro con `app.partida.seleccionar(...)`.
  - Según el **resultado** que devuelva el cerebro, reproduce un sonido:
    `voltear` (primera carta), `acierto` (pareja), `fallo` (no coinciden), o
    `victoria` (ganaste). Si ganaste, pasa a la pantalla de victoria.
  - Cuando hay desajuste, guarda el momento (`desajuste_en`) para que el
    "director" sepa cuándo ocultar las cartas.
- `dibujar(app)`: pinta el **marcador** (movimientos, parejas, tiempo y el botón
  Menú) y luego recorre la cuadrícula dibujando cada carta.
- `_dibujar_carta(...)`: si la carta está boca arriba, dibuja su imagen con un
  borde (verde si ya es pareja, amarillo si la acabas de voltear). Si está boca
  abajo, dibuja el dorso azul con un "?".

---

### 🎨 `interfaz/pantalla_victoria.py` — registrar al ganador

Aparece cuando ganas. Te felicita y te pide el nombre. Puedes **escribir uno
nuevo** o **elegir con un clic** uno que ya usaste antes.

- `_nombres_existentes(app)`: saca la lista de nombres ya usados, sin repetir y
  empezando por el más reciente (máximo 6). `reversed(...)` recorre la lista de
  atrás hacia delante (lo más nuevo primero).
- `_rects_nombres(...)`: calcula la posición de los botones de esos nombres, en
  dos columnas.
- `eventos(app, evento)`:
  - Clic en un nombre existente → lo usa y guarda el récord.
  - Teclado: Enter guarda; Backspace borra una letra; cualquier otra tecla
    **añade esa letra** al nombre (hasta 16 caracteres).
- `_guardar_ganador(app)`: crea el objeto `Puntuacion` con tu nombre,
  movimientos, tiempo, dificultad y fecha, lo **guarda** en la tabla y pasa a la
  pantalla de puntuaciones. Si no escribiste nada, te pone "Anonimo".
- `dibujar(app)`: pone una capa oscura semitransparente encima del tablero
  (efecto de "ventana emergente"), el "¡Ganaste!", tu resumen, la cajita de
  texto con un cursor que parpadea, y los botones de nombres.

---

### 🎨 `interfaz/pantalla_puntuaciones.py` — el Top 5

Muestra la tabla de mejores resultados.

- `eventos(app, evento)`: **cualquier** tecla o clic te devuelve al menú.
- `dibujar(app)`: escribe el título y, si hay récords, una tabla con posición,
  nombre, movimientos, tiempo y dificultad. Si no hay ninguno todavía, muestra
  "¡Sé el primero!". Los símbolos como `:<14` y `:>4` sirven para **alinear** las
  columnas (rellenar con espacios) y que la tabla quede ordenada.

---

### 🚪 Los puntos de entrada (`__main__.py` y `main.py`)

Un "punto de entrada" es **por dónde arranca** el programa.

- **`src/juego_memoria/__main__.py`**: permite ejecutar el juego con
  `python -m juego_memoria`. Solo crea la `Aplicacion` y llama a `ejecutar()`.
- **`main.py`** (en la raíz): pensado para arrancar fácil desde la consola con
  `python main.py`. Tiene un truco útil: si lo ejecutas con un Python que **no
  tiene Pygame**, se **relanza solo** usando el Python del entorno virtual
  `.venv`, donde sí está instalado. Así "simplemente funciona".

Ambos terminan haciendo lo mismo: crear `Aplicacion()` y llamar a `.ejecutar()`,
que enciende el bucle principal y arranca el juego en el menú.

---

## 7. Glosario rápido

| Palabra | Qué significa (en simple) |
|---|---|
| **Variable** | Una caja con nombre que guarda un dato. |
| **Función** | Una maquinita que recibe algo y hace un trabajo. |
| **Parámetro** | Lo que le pasas a una función entre paréntesis. |
| **`return`** | El resultado que devuelve una función. |
| **Clase** | El molde/plano para crear objetos. |
| **Objeto** | Una cosa concreta hecha con una clase. |
| **Atributo** | Un dato que guarda un objeto (su característica). |
| **Método** | Una acción que un objeto sabe hacer (función dentro de la clase). |
| **`self`** | "Yo mismo": el objeto concreto con el que se trabaja. |
| **`__init__`** | El constructor: se ejecuta al crear el objeto. |
| **Lista** | Una fila ordenada de cosas. Se cuenta desde 0. |
| **Diccionario** | Pares "nombre → valor", como una agenda. |
| **`bool`** | Verdadero (`True`) o falso (`False`). |
| **`None`** | "Nada / vacío". |
| **`if` / `else`** | Tomar una decisión. |
| **`for` / `while`** | Repetir cosas. |
| **`Enum`** | Lista cerrada de opciones con nombre. |
| **`@dataclass`** | Ayudante que crea por ti una clase de puros datos. |
| **Librería / módulo** | Caja de herramientas ya hecha que importas. |
| **Pygame** | La librería para ventana, dibujo, ratón y sonido. |
| **Bucle principal** | La repetición (60/seg) que mueve todo el juego. |
| **Evento** | Algo que hace el jugador (clic, tecla, cerrar). |
| **Estado / pantalla** | En cuál de las 4 vistas está el juego. |
| **Persistencia** | Guardar datos para que no se pierdan al cerrar. |
| **JSON** | Formato de texto para guardar datos de forma ordenada. |
| **FPS** | Cuántas imágenes por segundo (aquí 60). |
| **Píxel** | El puntito más pequeño de la pantalla. |

---

> ✅ **En una frase:** el "cerebro" (`tablero`, `partida`, `puntuaciones`) decide
> las **reglas** sin dibujar nada; la "cara" (`interfaz/`) **muestra** todo y
> escucha al jugador; y el "director" (`aplicacion.py`) los hace trabajar juntos
> 60 veces por segundo. ¡Eso es todo el juego! 🎉
