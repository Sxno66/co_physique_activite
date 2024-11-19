import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from scipy.io import wavfile
import pyaudio
import wave
import threading

# Variables pour stocker le fichier .wav et l'état de lecture
wav_file_path = None
audio_stream = None
is_playing = False
paused = False
current_position = 0  # Position actuelle de lecture (en nombre d'octets)

# Créer la fenêtre principale
root = tk.Tk()
root.title("Interface de Filtres Audio")
root.geometry("900x400")

# Fonction pour mettre à jour la valeur affichée du slider
def update_value(value, index):
    print(f"Valeur du slider {index+1} : {value}")
    slider_labels[index].config(text=f"Slider {index+1}: {int(float(value))}")

# Créer un cadre pour contenir les sliders côte à côte
frame_sliders = ttk.Frame(root)
frame_sliders.pack(pady=20)

# Créer des étiquettes pour afficher la valeur de chaque slider
slider_labels = []
sliders = []  # Liste pour stocker les sliders
for i in range(5):
    label = ttk.Label(frame_sliders, text=f"Slider {i+1}: 50")
    label.pack(side='left', padx=5)
    slider_labels.append(label)
    
    slider = ttk.Scale(
        frame_sliders,
        from_=100,
        to=0,
        orient='vertical',
        length=200,
        command=lambda value, i=i: update_value(value, i)
    )
    slider.set(50)  # Définir la valeur initiale à 50
    slider.pack(side='left', padx=5)
    sliders.append(slider)

# Fonction pour ouvrir le fichier .wav
def open_wav_file():
    global wav_file_path
    wav_file_path = filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
    if wav_file_path:
        print(f"Fichier sélectionné : {wav_file_path}")

# Fonction de filtrage numérique (Filtre simple IIR)
def filtreNum(data, a0, a1, b1, b2):
    filtered_data = np.zeros_like(data)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    filtered_data[2] = a0 * data[2] + a1 * data[1] + b1 * filtered_data[1] + b2 * filtered_data[0]
    for i in range(3, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

# Définir les filtres (coefficients)
filters = {
    "Filtre 1": (0.2183, -0.2183, 1.7505, -0.7661),
    "Filtre 2": (0.1941, -0.1941, 1.5568, -0.6813),
    "Filtre 3": (0.1589, -0.1589, 1.2747, -0.5578),
    "Filtre 4": (0.1249, -0.1249, 1.0023, -0.4386),
    "Filtre 5": (0.0972, -0.0972, 0.7800, -0.3413),
}

# Fonction pour ajuster l'amplification
def adjust_amplification(slider_value):
    amplification_factor = 1 + (slider_value / 100)  # Amplification simple entre 1 et 2
    return amplification_factor

# Fonction pour normaliser l'audio (afin d'éviter que le son devienne inaudible)
def normalize_audio(audio_data):
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        return audio_data / max_val  # Normaliser pour que l'amplitude soit entre -1 et 1
    else:
        return audio_data

# Fonction pour jouer l'audio avec des filtres appliqués
def play_audio():
    global is_playing, wav_file_path, paused
    if wav_file_path is None:
        print("Veuillez d'abord sélectionner un fichier WAV.")
        return
    
    if not is_playing:
        is_playing = True
        paused = False
        print("Lecture du fichier audio en cours...")
        threading.Thread(target=play_audio_thread).start()

# Fonction pour jouer l'audio en utilisant PyAudio avec les filtres
def play_audio_thread():
    global is_playing, paused, current_position
    wf = wave.open(wav_file_path, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    fs = wf.getframerate()

    wf.setpos(current_position)

    chunk = 1024
    data = wf.readframes(chunk)

    while data and is_playing:
        if paused:
            current_position = wf.tell()
            print(f"Lecture mise en pause à la position {current_position}")
            break
        
        # Convertir les données en tableau numpy pour appliquer les filtres
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Appliquer les filtres pour chaque slider
        combined_audio = np.zeros_like(audio_data, dtype=np.float32)
        for i, slider in enumerate(sliders):
            amplification_factor = adjust_amplification(slider.get())  # Récupérer la valeur du slider
            filter_name = f"Filtre {i+1}"
            if filter_name in filters:
                a0, a1, b1, b2 = filters[filter_name]
                filtered = filtreNum(audio_data, a0, a1, b1, b2)
                combined_audio += filtered * (slider.get() / 100)

        # Appliquer l'amplification
        audio_data = normalize_audio(combined_audio)  # Normaliser l'audio
        audio_data = (audio_data * 32767).astype(np.int16)  # Convertir en int16 pour PyAudio

        # Convertir les données filtrées en bytes pour les envoyer au flux audio
        filtered_data = audio_data.tobytes()
        stream.write(filtered_data)
        
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

    if not paused:
        is_playing = False
        print("Lecture terminée.")

# Fonction pour mettre en pause l'audio
def pause_audio():
    global is_playing, paused
    if is_playing:
        paused = True
        print("Lecture mise en pause.")
    else:
        print("Aucune lecture en cours.")

# Fonction pour reprendre la lecture après une pause
def resume_audio():
    global paused
    if paused:
        paused = False
        print("Reprise de la lecture.")
        threading.Thread(target=play_audio_thread).start()

# Créer les boutons pour ouvrir, jouer, mettre en pause, et reprendre la lecture
open_button = ttk.Button(root, text="Ouvrir fichier", command=open_wav_file)
open_button.pack(pady=10)

play_button = ttk.Button(root, text="Lire", command=play_audio)
play_button.pack(pady=10)

pause_button = ttk.Button(root, text="Pause", command=pause_audio)
pause_button.pack(pady=10)

resume_button = ttk.Button(root, text="Reprendre", command=resume_audio)
resume_button.pack(pady=10)

# Lancer l'interface graphique
root.mainloop()
