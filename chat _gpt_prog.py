import math
import threading
import numpy as np
import sounddevice as sd
from pynput import keyboard

# Pour couper l'écho du terminal (Linux/macOS)
import sys
try:
    import termios
except ImportError:
    termios = None

# ================== Réglages ==================
FREQ_LA = 440.0
TOUCHES_CLAVIER = ['q','z','s','e','d','f','t','g','y','h','u','j','k']
NOM_NOTES = ["do","do#","re","re#","mi","fa","fa#","sol","sol#","la","la#","si","do2"]
VOLUME = 0.2
ATTACK_SEC = 0.01
RELEASE_SEC = 0.05
BUFFER_FRAMES = 512
SR_CANDIDATES = [44100, 48000]
# ==============================================

# --- Fréquences tempérées à partir de A4=440 ---
OFFSETS = {
    "do":  -9,  # C4
    "do#": -8,
    "re":  -7,
    "re#": -6,
    "mi":  -5,
    "fa":  -4,
    "fa#": -3,
    "sol": -2,
    "sol#":-1,
    "la":   0,  # A4
    "la#":  1,
    "si":   2,
    "do2":  3,  # C5
}
dico_notes = {name: round(FREQ_LA * (2 ** (OFFSETS[name] / 12.0)), 6) for name in NOM_NOTES}

touches_to_notes = dict(zip(TOUCHES_CLAVIER, NOM_NOTES))
touches_enfoncees = set()

# --- État des oscillateurs ---
osc_lock = threading.Lock()
oscillateurs = {}  # note -> {phase,freq,amp,target,active}

def ensure_osc(note, sr):
    with osc_lock:
        if note not in oscillateurs:
            oscillateurs[note] = {
                "phase": 0.0,
                "freq": dico_notes[note],
                "amp": 0.0,
                "target": 1.0,
                "active": True,
            }
        else:
            oscillateurs[note]["target"] = 1.0
            oscillateurs[note]["active"] = True

def release_osc(note):
    with osc_lock:
        if note in oscillateurs:
            oscillateurs[note]["target"] = 0.0

def callback(outdata, frames, time_info, status):
    buffer = np.zeros(frames, dtype=np.float32)

    with osc_lock:
        local_notes = list(oscillateurs.items())

    if not local_notes:
        outdata[:] = buffer.reshape(-1, 1)
        return

    ramp_attack = 1.0 / max(1, int(ATTACK_SEC * current_sr))
    ramp_release = 1.0 / max(1, int(RELEASE_SEC * current_sr))

    with osc_lock:
        to_delete = []
        for note, osc in oscillateurs.items():
            freq = osc["freq"]
            phase = osc["phase"]
            amp = osc["amp"]
            target = osc["target"]
            omega = 2.0 * math.pi * freq / current_sr

            wave = np.empty(frames, dtype=np.float32)
            for i in range(frames):
                if target > amp:
                    amp = min(1.0, amp + ramp_attack)
                elif target < amp:
                    amp = max(0.0, amp - ramp_release)
                wave[i] = amp * math.sin(phase)
                phase += omega
                if phase > 2.0 * math.pi:
                    phase -= 2.0 * math.pi

            osc["phase"] = phase
            osc["amp"] = amp
            if osc["amp"] <= 1e-6 and osc["target"] == 0.0:
                to_delete.append(note)
            buffer += wave

        for note in to_delete:
            del oscillateurs[note]

    if len(local_notes) > 0:
        buffer *= (VOLUME / max(1, len(local_notes)))

    outdata[:] = buffer.reshape(-1, 1)

# --- Gestion clavier (pynput) ---
stop_flag = False

def on_press(key):
    global stop_flag
    try:
        k = key.char
        if k in touches_to_notes:
            note = touches_to_notes[k]
            touches_enfoncees.add(k)
            ensure_osc(note, current_sr)
    except AttributeError:
        if key == keyboard.Key.esc:
            stop_flag = True

def on_release(key):
    try:
        k = key.char
        if k in touches_enfoncees:
            touches_enfoncees.remove(k)
            note = touches_to_notes[k]
            release_osc(note)
    except AttributeError:
        pass

# --- Contexte: couper l'écho du terminal ---
class NoTerminalEcho:
    def __init__(self):
        self.enabled = False
        self.fd = None
        self.old = None

    def __enter__(self):
        if termios and sys.stdin.isatty():
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            new = termios.tcgetattr(self.fd)
            new[3] = new[3] & ~termios.ECHO  # lflag: unset ECHO
            termios.tcsetattr(self.fd, termios.TCSADRAIN, new)
            self.enabled = True
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.enabled and self.fd is not None and self.old is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)

# --- Ouverture du flux audio (essai 44.1k puis 48k) ---
stream = None
current_sr = None
last_err = None
for sr in SR_CANDIDATES:
    try:
        current_sr = sr
        stream = sd.OutputStream(
            samplerate=sr,
            channels=1,
            dtype='float32',
            blocksize=BUFFER_FRAMES,
            callback=callback,
        )
        stream.start()
        break
    except Exception as e:
        last_err = e
        stream = None
        continue

if stream is None:
    raise RuntimeError(f"Impossible d’ouvrir un flux audio. Dernière erreur: {last_err}")

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

try:
    with NoTerminalEcho():
        while not stop_flag:
            sd.sleep(50)
finally:
    listener.stop()
    if stream:
        stream.stop()
        stream.close()
