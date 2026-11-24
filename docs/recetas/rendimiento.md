# Cuidar la PC

Renderizar, transcribir y codificar usan todo el procesador que encuentran. Si la misma PC se está usando para editar o para jugar, se nota enseguida. Estas son las reglas para trabajar sin molestar.

## Reglas por defecto

- **Sin placa de video.** Render con `--no-browser-gpu` y modelos de IA en CPU.
- **Prioridad baja** para todo lo pesado.
- **Pocos hilos** por herramienta.
- **Un solo proceso pesado por vez.**
- **Avisar antes de un render largo** y hacer uno solo al final, en lugar de muchos de prueba. Las capturas de cuadros sueltos no molestan.

| Herramienta | Límite |
| --- | --- |
| ffmpeg | `-threads 2` |
| HyperFrames | `--workers 1` (hasta 3 si la PC está libre) |
| Whisper | `cpu_threads=2` |
| PyTorch | `torch.set_num_threads(2)` |
| librosa / numba | `OMP_NUM_THREADS=2`, `NUMBA_NUM_THREADS=2` |

## Prioridad baja en Windows

[`scripts/windows/bajo.ps1`](https://github.com/gastongv/codigo-y-agentes/blob/main/scripts/windows/bajo.ps1) corre una línea de comando con prioridad "por debajo de lo normal". Los procesos hijos la heredan, así que alcanza con envolver el comando principal.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File bajo.ps1 salida.log "npx hyperframes@0.8.150 render --no-browser-gpu --workers 1 -o renders/video.mp4"
```

!!! warning "Por debajo de lo normal, no inactiva"
    Con la prioridad más baja (`Idle`, o `start /low`) y la PC al 87 % de uso, una validación que tarda segundos quedó trabada diez minutos. `BelowNormal` cede el paso sin quedarse sin turno.

Desde Python, en Windows, el equivalente es pasar `creationflags=0x00004000` a `subprocess.run`.

## Cuando hay apuro

Si lo que importa es terminar rápido y la PC está disponible, se invierte todo: placa de video y varios procesos.

```bash
npx hyperframes@0.8.150 render --gpu --browser-gpu --workers 6 -o renders/video.mp4
```

| Video | Sin placa | Con placa y 6 procesos |
| --- | --- | --- |
| 110 s a 1080 | 6 a 7 min | 3 min 15 s |
| 37 s a 1080 | sin medir | 1 min 30 s |

Con `h264_nvenc`, la versión liviana se codifica en segundos.

Es una decisión de cada sesión: por defecto, sin placa.

## Qué tarda cada cosa

Sirve para avisar con un número y no con "un rato":

| Tarea | Tiempo medido |
| --- | --- |
| Render de un spot de 48 s con filmación real, sin placa, 3 procesos | Unos 5 min |
| Render 4K completo de un video de más de un minuto | 10 min o más |
| Escena 3D de 35 s a 2160×3840 (con placa) | Unos 2 min |
| Un render que se pasó a HDR por un clip mal marcado | Más de 10 min, y sale mal |
