#!/bin/bash
# Versión liviana para WhatsApp / Instagram / TikTok: H.264 2 pasadas, 2 hilos, audio a -14 LUFS. Uso: liviano.sh <in> <out> <kbps>
set -e; t=$(mktemp -d); c=(-c:v libx264 -preset slow -profile:v high -level 4.1 -b:v ${3}k -maxrate $(( $3*2 ))k -bufsize $(( $3*4 ))k -g 60 -threads 2 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709)
ffmpeg -v error -y -i "$1" "${c[@]}" -pass 1 -passlogfile "$t/p" -an -f mp4 NUL
ffmpeg -v error -y -i "$1" "${c[@]}" -pass 2 -passlogfile "$t/p" -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 128k -ar 48000 -movflags +faststart "$2"; rm -rf "$t"
