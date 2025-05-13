import numpy as np
from scipy.io import wavfile as wav

class Distortion:
    @staticmethod
    def reduce_distortion(audio, threshold=0.1):
        spectrum = np.fft.fft(audio)

        avg_amplitude = np.mean(np.abs(spectrum))
        
        # Appliquer un masque pour les parties du spectre au-delà du seuil
        mask = np.abs(spectrum) > avg_amplitude * (1 + threshold)
        
        # Réduire l'amplitude de ces parties
        spectrum[mask] *= 0.8
        
        processed_audio = np.fft.ifft(spectrum).real

        return np.int16(processed_audio)

# def process_audio(input_file, output_file, threshold=0.1):
#     # Charger un fichier audio WAV
#     sample_rate, audio = wav.read(input_file)

#     # Vérifier si le signal audio est stéréo et le convertir en mono si nécessaire
#     if len(audio.shape) > 1:
#         audio = np.mean(audio, axis=1)  # Moyenne des canaux pour obtenir un signal mono

#     # Convertir le signal audio en domaine fréquentiel avec FFT
#     # spectrum = np.fft.fft(audio)

#     # Appliquer le traitement antidistorsion
#     processed_spectrum = reduce_distortion(audio, threshold)

#     # Revenir au domaine temporel en appliquant la transformée inverse de Fourier
#     # processed_audio = np.fft.ifft(processed_spectrum).real

#     # Sauvegarder l'audio corrigé dans un fichier WAV
#     # wav.write(output_file, sample_rate, processed_audio.astype(np.int16))
#     wav.write(output_file, sample_rate, processed_spectrum)

#     print(f"Traitement antidistorsion terminé. Fichier sauvegardé sous : {output_file}")


# # Exemple d'utilisation
# process_audio("audio_bruite.wav", "output_audio_corrected.wav", threshold=0.1)
