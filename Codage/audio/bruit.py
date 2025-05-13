import numpy as np
import scipy.io.wavfile as wav

class Bruit:
    @staticmethod
    def reduce_noise(audio, sr, noise_threshold=0.02):
        spectrum = np.fft.rfft(audio)
        
        # Appliquer un filtre passe-haut pour supprimer les basses fréquences (ex. bruit de fond)
        freqs = np.fft.rfftfreq(len(audio), d=1/sr)
        spectrum[freqs < 100] = 0  # Supprime les fréquences inférieures à 100 Hz

        # Réduction du bruit en atténuant les faibles amplitudes (souffle, bourdonnement)
        magnitude = np.abs(spectrum)
        spectrum[magnitude < noise_threshold * np.max(magnitude)] = 0

        filtered_audio = np.fft.irfft(spectrum)

        return np.int16(filtered_audio)

# # Charger un fichier audio WAV
# sample_rate, audio = wav.read("audio_bruite.wav")

# # Vérifier si audio est stéréo et convertir en mono
# if len(audio.shape) > 1:
#     audio = np.mean(audio, axis=1)

# # Appliquer la réduction de bruit
# filtered_audio = reduce_noise(audio, sample_rate)

# noise_only = audio - filtered_audio
# # Sauvegarder l'audio filtré
# wav.write("output_filtered.wav", sample_rate, filtered_audio)
# # bruit seulement
# wav.write("output_noise.wav", sample_rate, np.int16(noise_only))