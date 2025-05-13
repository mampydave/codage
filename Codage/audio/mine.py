import cmath
import math

def read_wav(filename):
    with open(filename, "rb") as f:
        data = f.read()
        sample_rate = int.from_bytes(data[24:28], "little")
        samples = []
        for i in range(44, len(data), 2):
            sample = int.from_bytes(data[i:i+2],"little", signed=True)
            samples.append(sample)
    return samples, sample_rate

def dft(signal):
    N = len(signal)
    if N <= 1:
        return signal
    
    even = dft(signal[0:2])
    odd = dft(signal[1:2])
    
    T = [cmath.exp(-2j * cmath.pi * k / N) * odd[k] for k in range(N // 2)]
    
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]
    # real_part = [0] * N
    # imag_part = [0] * N
    # magnitude = [0] * N
    
    # for k in range(N):  # Parcourir les fréquences
    #     for n in range(N):  # Parcourir les échantillons
    #         angle = -2 * math.pi * k * n / N
    #         real_part[k] += signal[n] * math.cos(angle)
    #         imag_part[k] += signal[n] * math.sin(angle)
        
    #     magnitude[k] = math.sqrt(real_part[k]**2 + imag_part[k]**2)
    
    # return magnitude

def noise_reduction_auto(magnitude, phase, sample_rate, noise_threshold=0.05):    
    # 1. Calcul du seuil de bruit basé sur l'amplitude des fréquences
    avg_magnitude = np.mean(magnitude)
    std_magnitude = np.std(magnitude)  # Calcul de l'écart-type
    dynamic_threshold = avg_magnitude + noise_threshold * std_magnitude  # Seuil dynamique basé sur l'écart-type
    
    # 2. Appliquer un filtre : Réduire ou supprimer les fréquences de bruit
    noise_mask = magnitude < dynamic_threshold  # Identifie les fréquences faibles
    magnitude[noise_mask] *= 0.3  # Mise à zéro des fréquences de bruit
    
    # 3. Filtrage passe-bas plus strict : supprimer les fréquences élevées (filtres adaptés)
    cutoff_frequency = int(sample_rate / 16)  # Couper après 1/16 de la fréquence d'échantillonnage
    magnitude[cutoff_frequency:] = 0  # Appliquer le filtre passe-bas strict
    
    # 4. Retour au domaine temporel avec la transformée inverse de Fourier
    # Nous reconstruisons le spectre en combinant la magnitude nettoyée avec la phase originale
    cleaned_spectrum = magnitude * np.exp(1j * phase)  # Recombiner la magnitude nettoyée et la phase
    filtered_signal = np.fft.ifft(cleaned_spectrum).real  # Nous prenons la partie réelle
    
    # 5. Normalisation du signal pour éviter toute saturation (plage -32768 à 32767)
    filtered_signal = np.clip(filtered_signal, -32768, 32767)  # Limiter à 16 bits
    filtered_signal = filtered_signal.astype(np.int16)  # Conversion en entier 16 bits
    
    return filtered_signal

samples, sample_rate = read_wav("output_processed.wav")
spectrum = dft(samples)
print(f"signal charge : {len(samples)} echantillon a {sample_rate} Hz AVEC spectrum : {spectrum}")
