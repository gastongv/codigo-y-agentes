#!/bin/bash
# Master de audio para redes sin recomprimir la imagen.
# Mide el volumen integrado, aplica la ganancia que falta para llegar al objetivo y limita con sobremuestreo
# (el limitador ve los picos reales entre muestras). No usa loudnorm de una pasada, que deja el pico demasiado alto.
# Uso: master.sh <entrada.mp4> <salida.mp4> [LUFS objetivo, por defecto -14]
set -e
in="$1"; out="$2"; obj="${3:--14}"
medido=$(ffmpeg -hide_banner -nostats -i "$in" -vn -af ebur128=framelog=quiet -f null - 2>&1 | awk '$1=="I:" {v=$2} END {print v}')
gan=$(awk -v o="$obj" -v m="$medido" 'BEGIN {printf "%.2f", o - m}')
echo "medido: ${medido} LUFS | ganancia: ${gan} dB"
ffmpeg -v error -y -i "$in" -c:v copy \
  -af "volume=${gan}dB,aresample=192000,alimiter=limit=0.78:level=false,aresample=48000" \
  -c:a aac -b:a 160k -movflags +faststart "$out"
