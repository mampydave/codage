import numpy as np

class Amplifier:
    @staticmethod
    def dft(signal):
        spectrum = np.fft.fft(signal)
        magnitude = np.abs(spectrum)
        phase = np.angle(spectrum)
        return magnitude, phase, spectrum

    @staticmethod
    def multiplier(magnitude, gain):
        magnitude = magnitude.real.astype(np.float32)  
        return magnitude * gain

    @staticmethod
    def process_block(i, samples, block_size, sample_rate, gain):
        block = samples[i:i + block_size]
        magnitude, phase, spectrum = Amplifier.dft(block) 
        amplified_magnitude = Amplifier.multiplier(magnitude, gain)
        
        processed_block = amplified_magnitude
        return processed_block[:len(block)]

    @staticmethod
    def amplify(samples, sample_rate, gain):
        processed_signal = np.zeros_like(samples, dtype=np.int16)
        block_size = 4096  # Traitement par blocs
        # Traitement des blocs
        for i in range(0, len(samples), block_size):
            processed_block = Amplifier.process_block(i, samples, block_size, sample_rate, gain)
            processed_signal[i:i + block_size] = processed_block
            print(f"Processing block {i + 1}/{len(samples)}...")        
        
        return processed_signal

    @staticmethod
    def speed_up_with_sampling_rate(signal, sample_rate, speed_factor):
        """Accélère le signal audio en rééchantillonnant à un taux plus élevé"""
        # Calculer le nouvel échantillonnage
        new_sample_rate = sample_rate * speed_factor
        # Calculer la nouvelle longueur du signal
        new_length = int(len(signal) / speed_factor)
        
        # Rééchantillonner en supprimant des échantillons
        indices = np.arange(0, len(signal), speed_factor).astype(int)
        speeded_up_signal = signal[indices[:new_length]]
        
        # Optionnel : Renormaliser les valeurs entre -32768 et 32767
        speeded_up_signal = np.clip(speeded_up_signal, -32768, 32767).astype(np.int16)
        
        return speeded_up_signal


