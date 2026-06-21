# Lanzador del juego para PowerShell.
# Usa SIEMPRE el Python del entorno virtual (.venv), sin importar la carpeta actual.
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$raiz\.venv\Scripts\python.exe" -m juego_memoria @args
