import math
import numpy as np
import sounddevice as sd
import keyboard
import time

# Fréquence de référence (La 440 Hz)
freq_la = 440

# Noms des notes (1 octave chromatique)
nom_notes = ["la", "la#", "si", "do", "do#", "re", "re#", "mi", "fa", "fa#", "sol", "sol#", "do2"]

# Calcul des fréquences relatives à La
dico_notes = {}
for i in range(12):
    freq = freq_la * math.pow(2, i / 12)
    while freq > freq_la * 2:
        freq /= 2
    freq = round(freq, 3)
    dico_notes[nom_notes[i]] = freq

# Mappage touches clavier → noms des notes
touches_clavier = ['q', 'z', 's', 'e', 'd', 'f', 't', 'g', 'y', 'h', 'u', 'j', 'k']

#rajout d'un do
dico_notes["do2"] = dico_notes["do"] * 2

touches_to_notes = dict(zip(touches_clavier, nom_notes))

# Liste des touches actuellement jouées
touches_enfoncees = set()

# Fonction pour générer un son contenant plusieurs fréquences superposées
def play_multiple_frequencies(frequencies, duration=0.2, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.zeros_like(t)
    
    for freq in frequencies:
        wave += 0.3 * np.sin(2 * np.pi * freq * t)  # 0.3 pour éviter saturation

    wave = np.clip(wave, -1, 1)  # éviter les débordements
    sd.play(wave, samplerate=sample_rate)

print("Touches : " + ", ".join(touches_clavier))
print("ESC pour quitter.")

# Boucle principale
while True:
    notes_actives = []

    for touche in touches_clavier:
        if keyboard.is_pressed(touche):
            if touche not in touches_enfoncees:
                touches_enfoncees.add(touche)
        else:
            if touche in touches_enfoncees:
                touches_enfoncees.remove(touche)

    # Générer la liste des fréquences à jouer
    for touche in touches_enfoncees:
        note = touches_to_notes[touche]
        freq = dico_notes[note]
        notes_actives.append(freq)

    if notes_actives:
        play_multiple_frequencies(notes_actives)

    # Sortie propre
    if keyboard.is_pressed('esc'):
        print("👋 Fin du concert.")
        break

    time.sleep(0.05)

