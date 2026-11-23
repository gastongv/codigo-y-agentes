#!/bin/bash
# Uso: achicar.sh <entrada.mp4> <salida.mp4> <kbps de video>
# H.264 High 1080x1920 30 fps en dos pasadas, AAC 128k, faststart, sin GPU. hqdn3d suave quita el grano fino (lo que más pesa).
set -e
in="$1"; out="$2"; v="$3"; tmp=$(mktemp -d)
vf="hqdn3d=1.2:1.2:4:4,format=yuv420p"
common=(-c:v libx264 -preset slow -profile:v high -level 4.1 -b:v ${v}k -maxrate $((v*2))k -bufsize $((v*4))k -g 60 -threads 6 -vf "$vf" -colorspace bt709 -color_primaries bt709 -color_trc bt709)
ffmpeg -v error -y -i "$in" "${common[@]}" -pass 1 -passlogfile "$tmp/p" -an -f mp4 NUL
ffmpeg -v error -y -i "$in" "${common[@]}" -pass 2 -passlogfile "$tmp/p" -c:a aac -b:a 128k -ar 48000 -movflags +faststart "$out"
rm -rf "$tmp"
