import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Fonction pour normaliser les signaux
def normalize(signal):
    return signal / np.max(np.abs(signal))

# Conversion en dBV
def to_dbv(magnitude, epsilon=1e-12):
    return 20 * np.log10(np.maximum(magnitude, epsilon))

# Coefficients pour différents filtres
def filtreNum(data, a0, a1, b1, b2):
    filtered_data = np.zeros_like(data)
    filtered_data[0] = a0 * data[0]
    filtered_data[1] = a0 * data[1] + a1 * data[0] + b1 * filtered_data[0]
    filtered_data[2] = a0 * data[2] + a1 * data[1] + b1 * filtered_data[1] + b2 * filtered_data[0]
    for i in range(3, len(data)):
        filtered_data[i] = a0 * data[i] + a1 * data[i - 1] + b1 * filtered_data[i - 1] + b2 * filtered_data[i - 2]
    return filtered_data

# Définir les filtres
filters = {
    "Filtre 9": (0.0972, -0.0972, 0.7800, -0.3413),
    "Filtre 7": (0.1249, -0.1249, 1.0023, -0.4386),
    "Filtre 5": (0.1589, -0.1589, 1.2747, -0.5578),
    "Filtre 3": (0.1941, -0.1941, 1.5568, -0.6813),
    "Filtre 1": (0.2183, -0.2183, 1.7505, -0.7661),
}

# Génération du signal d'entrée
type = 2  # 0: Sinusoïde, 1: WAV, 2: Impulsion
if type == 0: 
    freq_ech = 44100
    f_sin = 2000
    duree = 1
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)
    data = np.sin(2 * np.pi * f_sin * t)

elif type == 1:
    freq_ech, data = wavfile.read('LW_20M_amis.wav')
    t = np.linspace(0, len(data) / freq_ech, len(data), endpoint=False)
else:
    freq_ech = 44100
    duree = 3
    data = np.zeros(freq_ech * duree)
    data[0] = 1
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)

if len(data.shape) > 1:
    data = data[:, 0]

# Appliquer les filtres
filtered_signals = {}
for name, (a0, a1, b1, b2) in filters.items():
    filtered_signal = filtreNum(data, a0, a1, b1, b2)
    filtered_signals[name] = normalize(filtered_signal)

# FFT
fft_result = np.abs(np.fft.fft(data))
fft_results = {name: np.abs(np.fft.fft(filtered_signal)) for name, filtered_signal in filtered_signals.items()}

# Conversion des FFT en dBV
fft_dbv = to_dbv(fft_result)
fft_dbv_results = {name: to_dbv(fft_filtered) for name, fft_filtered in fft_results.items()}

# Limiter la plage de fréquences et personnaliser l'affichage
freq_min = 10  # Fréquence minimale en Hz
freq_max = 20000  # Fréquence maximale en Hz

frequences = np.fft.fftfreq(len(fft_result), d=1 / freq_ech)
valid_indices = (frequences > freq_min) & (frequences < freq_max)
frequences_limited = frequences[valid_indices]
fft_dbv_limited = fft_dbv[valid_indices]
fft_dbv_results_limited = {name: fft_dbv[valid_indices] for name, fft_dbv in fft_dbv_results.items()}

# Affichage des graphiques
plt.figure(figsize=(12, 8))

# Graphique 1 : Signal temporel
plt.subplot(2, 1, 1)
plt.plot(t, data, label='Signal Origine', color='black')
for name, filtered_signal in filtered_signals.items():
    plt.plot(t, filtered_signal, label=name, linestyle='--')
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude')
plt.title('Signal temporel avec différents filtres')
plt.legend()

# Graphique 2 : Spectre de Fourier (en dBV) avec plage de fréquences limitée
plt.subplot(2, 1, 2)
plt.plot(frequences_limited, fft_dbv_limited, label='FFT Original')
for name, fft_filtered_dbv in fft_dbv_results_limited.items():
    plt.plot(frequences_limited, fft_filtered_dbv, label=f'FFT {name}')
plt.xscale('log')  # Échelle logarithmique pour l'axe des fréquences
plt.xticks(
    [10, 100, 1000, 10000],  # Ticks personnalisés
    ['10 Hz', '100 Hz', '1 kHz', '10 kHz']  # Labels correspondants
)
plt.xlabel('Fréquence [Hz]')
plt.ylabel('Magnitude (dBV)')
plt.title('Spectre de Fourier en dBV des signaux filtrés (10 Hz à 20 kHz)')
plt.legend()

plt.tight_layout()
plt.show()
