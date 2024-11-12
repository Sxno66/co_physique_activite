import tkinter as tk
from tkinter import ttk

# Créer la fenetre principale
root = tk.Tk()
root.title("Slider Simple")
root.geometry("800x400")

# Fonction pour mettre à jour la valeur affichée du slider
def update_value(value):
    print(f"Valeur : {slider1.get()}")
    label.config(text=f"Valeur: {int(float(value))}")

def affichageSlider(value):
    print(f"Valeur du slider: {slider1.get()}")

# Créer un label pour afficher la valeur du slider
label = ttk.Label(root, text="Valeur: 50")
label.pack(pady=10)

# Créer un cadre pour contenir les sliders côte à côte
frame_sliders = ttk.Frame(root)
frame_sliders.pack(pady=20)

# Créer cinq sliders verticaux
sliders = []  # Liste pour stocker les sliders
for i in range(5):
    slider = ttk.Scale(
        frame_sliders,
        from_=0,
        to=100,
        orient='vertical',
        length=200,  # Longueur ajustée pour 5 sliders
        command=update_value
    )
    slider.set(50)
    slider.pack(side='left', padx=5)  # Ajout d'un peu d'espace entre les sliders
    sliders.append(slider)

# Créer un bouton
button = ttk.Button(root, text="Afficher la valeur", command=affichageSlider)
button.pack(pady=20)

# Lancement de la boucle principale
root.mainloop()
