import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Créer la fenêtre principale
root = tk.Tk()
root.title("Interface avec Sliders et Sélecteur de Fichier")
root.geometry("800x500")

# Variable pour stocker le chemin du fichier choisi
selected_file = tk.StringVar()

# Fonction pour mettre à jour la valeur affichée des sliders et les afficher dans le terminal
def update_value(index, value):
    print(f"Slider {index + 1}: Valeur = {float(value):.2f}")

# Fonction pour afficher toutes les valeurs des sliders
def affichageSliders():
    print("\nValeurs actuelles des sliders :")
    for i, slider in enumerate(sliders):
        print(f"Slider {i + 1}: {slider.get():.2f}")

# Fonction pour choisir un fichier .wav
def choose_file():
    file_path = filedialog.askopenfilename(
        title="Choisir un fichier .wav",
        filetypes=[("Fichiers WAV", "*.wav")]  # Limiter aux fichiers .wav
    )
    if file_path:
        selected_file.set(file_path)
        print(f"Fichier sélectionné : {file_path}")
        file_label.config(text=f"Fichier sélectionné : {file_path}")

# Créer un label pour afficher la valeur du slider
file_label = ttk.Label(root, text="Aucun fichier sélectionné")
file_label.pack(pady=10)

# Créer un cadre pour contenir les sliders côte à côte
frame_sliders = ttk.Frame(root)
frame_sliders.pack(pady=20)

# Créer les sliders avec un label pour chaque
sliders = []  # Liste pour stocker les sliders
for i in range(5):
    # Cadre pour chaque slider (pour aligner le label au-dessus du slider)
    slider_frame = ttk.Frame(frame_sliders)
    slider_frame.pack(side='left', padx=10)

    # Label pour le numéro du slider
    label = ttk.Label(slider_frame, text=f"Slider {i + 1}")
    label.pack()

    # Slider vertical avec valeurs allant de 50 à 100 vers le haut et de 50 à 0 vers le bas
    slider = ttk.Scale(
        slider_frame,
        from_=100,   # Valeur la plus haute en haut
        to=0,        # Valeur la plus basse en bas
        orient='vertical',
        length=200,
        command=lambda value, index=i: update_value(index, value)  # Passer l'index du slider
    )
    slider.set(50)  # Initialiser à 50
    slider.pack()

    sliders.append(slider)

# Créer un bouton pour afficher les valeurs des sliders
button = ttk.Button(root, text="Afficher les valeurs des sliders", command=affichageSliders)
button.pack(pady=10)

# Créer un bouton pour choisir un fichier .wav
file_button = ttk.Button(root, text="Choisir un fichier .wav", command=choose_file)
file_button.pack(pady=10)

# Lancement de la boucle principale
root.mainloop()
