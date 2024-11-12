import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Coefficients pour différents filtres
def filtreNumTemp9(data):
    a0, a1, b1, b2 = 0.0972, -0.0972, 0.7800, -0.3413
    filtered_data = np.zeros_like(data)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    filtered_data[2] = a0 * data[2] + a1 * data[1] + b1 * filtered_data[1] + b2 * filtered_data[0]
    for i in range(3, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp7(data):
    a0, a1, b1, b2 = 0.1249, -0.1249, 1.0023, -0.4386
    filtered_data = np.zeros_like(data)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    filtered_data[2] = a0 * data[2] + a1 * data[1] + b1 * filtered_data[1] + b2 * filtered_data[0]
    for i in range(3, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp5(data):
    a0, a1, b1, b2 = 0.1589, -0.1589, 1.2747, -0.5578
    filtered_data = np.zeros_like(data)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    filtered_data[2] = a0 * data[2] + a1 * data[1] + b1 * filtered_data[1] + b2 * filtered_data[0]
    for i in range(3, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp3(data):
    a0, a1, b1, b2 = 0.1941, -0.1941, 1.5568, -0.6813
    filtered_data = np.zeros_like(data)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    filtered_data[2] = a0 * data[2] + a1 * data[1] + b1 * filtered_data[1] + b2 * filtered_data[0]
    for i in range(3, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

def filtreNumTemp1(data):
    a0, a1, b1, b2 = 0.2183, -0.2183, 1.7505, -0.7661
    filtered_data = np.zeros_like(data)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    filtered_data[2] = a0 * data[2] + a1 * data[1] + b1 * filtered_data[1] + b2 * filtered_data[0]
    for i in range(3, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

# 3 exemples de données d'entrée
type = 2
creationWavFiltre = False

if type == 0: 
    # Signal sinusoïdal
    freq_ech = 44100
    f_sin = 2000
    duree = 1
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)
    data = np.sin(2 * np.pi * f_sin * t)

elif type == 1:
    # Fichier wav
    freq_ech, data = wavfile.read('LW_20M_amis.wav')
    t = np.linspace(0, len(data) / freq_ech, len(data), endpoint=False)
    creationWavFiltre = True

else:
    # Impulsion
    freq_ech = 44100
    duree = 3
    data = np.zeros(freq_ech * duree)
    data[0] = 1
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)

# Vérifier si le fichier est stéréo ou mono
if len(data.shape) > 1:
    data = data[:, 0]  # Prendre le canal gauche si stéréo

# Appliquer les filtres
signal_filtre1 = filtreNumTemp9(data)
signal_filtre2 = filtreNumTemp7(data)
signal_filtre3 = filtreNumTemp5(data)
signal_filtre4 = filtreNumTemp3(data)
signal_filtre5 = filtreNumTemp1(data)

# Calculer la FFT des signaux
fft_result = np.fft.fft(data)
fft_result_filtre1 = np.fft.fft(signal_filtre1)
fft_result_filtre2 = np.fft.fft(signal_filtre2)
fft_result_filtre3 = np.fft.fft(signal_filtre3)
fft_result_filtre4 = np.fft.fft(signal_filtre4)
fft_result_filtre5 = np.fft.fft(signal_filtre5)

# Créer les graphiques
plt.figure(figsize=(12, 8))

# Graphique 1 : Signal temporel
plt.subplot(2, 1, 1)
plt.plot(t, data, label='Signal Origine', color='black')
plt.plot(t, signal_filtre1, label='Filtre 9', linestyle='--')
plt.plot(t, signal_filtre2, label='Filtre 7', linestyle='--')
plt.plot(t, signal_filtre3, label='Filtre 5', linestyle='--')
plt.plot(t, signal_filtre4, label='Filtre 3', linestyle='--')
plt.plot(t, signal_filtre5, label='Filtre 1', linestyle='--')
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude')
plt.title('Signal temporel avec différents filtres')
plt.legend()

# Graphique 2 : Spectre de Fourier
frequences = np.fft.fftfreq(len(fft_result), d=1 / freq_ech)

plt.subplot(2, 1, 2)
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result)[:len(fft_result)//2], label='FFT Original')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_filtre1)[:len(fft_result_filtre1)//2], label='FFT Filtre 9')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_filtre2)[:len(fft_result_filtre2)//2], label='FFT Filtre 7')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_filtre3)[:len(fft_result_filtre3)//2], label='FFT Filtre 5')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_filtre4)[:len(fft_result_filtre4)//2], label='FFT Filtre 3')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_filtre5)[:len(fft_result_filtre5)//2], label='FFT Filtre 1')
plt.xscale('log')  # Échelle logarithmique pour l'axe des x (fréquences)
plt.yscale('log')  # Échelle logarithmique pour l'axe des y (amplitude)
plt.xlabel('Fréquence [Hz]')
plt.ylabel('Magnitude')
plt.title('Spectre de Fourier des signaux filtrés')
plt.legend()

plt.tight_layout()
plt.show()

# Sauvegarde du fichier audio filtré si nécessaire
if creationWavFiltre:
    wavfile.write("signal_filtre.wav", freq_ech, signal_filtre1.astype(np.float32))  # Exemple de sauvegarde
