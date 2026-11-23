"""Parche edge-tts (PR rany2/edge-tts#491): desde oct-2026 el host viejo da 403 al sintetizar."""
import edge_tts.communicate as _cm
from edge_tts.constants import TRUSTED_CLIENT_TOKEN as _T
_cm.WSS_URL = f"wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1?Ocp-Apim-Subscription-Key={_T}"
