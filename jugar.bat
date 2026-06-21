@echo off
REM Lanzador del juego: usa SIEMPRE el Python del entorno virtual (.venv),
REM sin importar desde que carpeta se ejecute (incluso con doble clic).
cd /d "%~dp0"
".venv\Scripts\python.exe" -m juego_memoria %*
