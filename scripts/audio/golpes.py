# Tempo y golpes de la música para sincronizar las palabras. Elige la ventana de 17 s con más energía que empiece en un golpe.
# Uso: python golpes.py <mp3>  → golpes.json (al lado del script). Requiere librosa y numpy.
import json, os, sys
os.environ["OMP_NUM_THREADS"] = "2"; os.environ["NUMBA_NUM_THREADS"] = "2"
import librosa, numpy as np
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
rms = librosa.feature.rms(y=y, hop_length=512)[0]; tr = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)
VENT = 17.0
mejor = max((b for b in beats if b + VENT < tr[-1]), key=lambda b: rms[(tr >= b) & (tr < b + VENT)].mean() - 0.6 * rms[(tr >= b) & (tr < b + VENT)].std())
sel = [round(float(b - mejor), 3) for b in beats if mejor <= b < mejor + VENT]
json.dump({"tempo": float(np.atleast_1d(tempo)[0]), "inicio": round(float(mejor), 3), "golpes": sel}, open(os.path.join(os.path.dirname(__file__), "golpes.json"), "w"))
print("tempo", np.atleast_1d(tempo)[0], "inicio", mejor, "golpes", len(sel), sel[:12])
