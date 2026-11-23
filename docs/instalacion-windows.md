# Instalación en Windows

Lo que sigue es lo que hizo falta en una PC con Windows 11. Casi todos los tropiezos son de Windows y no de las herramientas.

## Lo básico

```powershell
winget install Gyan.FFmpeg
winget install OpenJS.NodeJS
winget install Python.Python.3.12
pip install edge-tts
```

HyperFrames no se instala: se llama con `npx`, fijando la versión para que un proyecto no cambie de comportamiento con el tiempo.

```powershell
npx hyperframes@0.8.150 doctor    # revisa ffmpeg, Chrome y dependencias
npx hyperframes@0.8.150 preview   # vista previa en el navegador
npx hyperframes@0.8.150 check     # valida la composición
npx hyperframes@0.8.150 render    # genera el MP4
```

Conviene correr `doctor` antes del primer render de cada sesión.

## FFmpeg en Git Bash

Git Bash no ve el `ffmpeg` que instala winget. Hay que agregar al `PATH` la carpeta de enlaces de winget o la carpeta `bin` del paquete:

```bash
export PATH="$PATH:/c/Users/<usuario>/AppData/Local/Microsoft/WinGet/Links"
```

## `python3` apunta a la Microsoft Store

En Windows, `python3` suele ser un alias que abre la tienda en lugar de correr Python, y las herramientas que lo llaman fallan con "Python was not found".

Arreglo sin permisos de administrador: copiar `python.exe` con el nombre `python3.exe` a una carpeta propia y ponerla primera en el `PATH` del usuario.

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.local\pyshim"
Copy-Item "C:\Python312\python.exe" "$env:USERPROFILE\.local\pyshim\python3.exe"
Get-Command python3 -All   # la copia tiene que figurar primera
```

Si Python se actualiza, hay que repetir la copia.

## Saltos de línea

Con `core.autocrlf=true`, Git convierte los archivos a CRLF al clonar. En los scripts de Bash eso mete un `\r` invisible en los valores (por ejemplo en `-threads 2\r`) y los comandos fallan sin un error claro. En los repositorios de herramientas conviene:

```bash
git config core.autocrlf false
```

## Rutas en Git Bash

Un argumento que empieza con `/` se convierte en una ruta de Windows: `/x` pasa a ser `C:/Program Files/Git/x`. Afecta a cualquier comando que reciba rutas de una aplicación web o de una API como argumento.

## PowerShell y JSON

PowerShell 5.1 le quita las comillas al JSON que se pasa en la línea de comandos. Para las variables de un render, usar un archivo:

```powershell
npx hyperframes@0.8.150 render --variables-file variables.json
```

## Entornos de Python que esperan Linux

Algunos scripts buscan el intérprete en `venv/bin/python3`, que en Windows no existe: está en `venv\Scripts\python.exe`. Se resuelve con un enlace de carpeta (`bin` que apunta a `Scripts`) y una copia de `python.exe` llamada `python3.exe`.

`faster-whisper` con placa de video puede no encontrar `cublas64_12.dll`. Las bibliotecas ya vienen con `torch`: alcanza con enlazarlas desde `torch/lib` a la carpeta de `ctranslate2` del mismo entorno.

## WSL se apaga solo

Si una base de datos corre dentro de WSL (por ejemplo, el Postgres de la aplicación que se va a capturar), WSL se apaga cuando no queda ninguna sesión abierta y la base se cae. Para mantenerlo prendido durante la sesión de trabajo:

```powershell
wsl -d Ubuntu -- bash -c "sleep 14400"
```
