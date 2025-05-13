import numpy as np

def read_wav(filename):
    with open(filename, "rb") as f:
        header = f.read(44)
        sample_rate = int.from_bytes(header[24:28], byteorder="little")
        data = np.frombuffer(f.read(), dtype=np.int16)
    return sample_rate, data

def dft(signal):
    spectrum = np.fft.fft(signal)
    magnitude = np.abs(spectrum)
    phase = np.angle(spectrum)
    return magnitude, phase

def idft(magnitude, phase):
    spectrum = magnitude * np.exp(1j * phase)
    return np.fft.ifft(spectrum).real.astype(np.int16)

def amplify(magnitude, gain):
    amplified = magnitude * gain
    max_value = np.max(amplified)
    if max_value > 32767:  # Éviter l'écrêtage
        amplified = (amplified / max_value) * 32767
    return amplified

def noise_reduction(spectrum, low_cutoff, high_cutoff, sample_rate, reduction_factor=0.1):
    N = len(spectrum)
    freqs = np.fft.fftfreq(N, d=1/sample_rate)  # Fréquences réelles associées au spectre

    # Création d'un masque avec transition douce pour éviter les coupures brutales
    mask = np.ones(N)
    mask[np.abs(freqs) < low_cutoff] *= reduction_factor  # Atténuer les basses fréquences
    mask[np.abs(freqs) > high_cutoff] *= reduction_factor  # Atténuer les hautes fréquences

    return spectrum * mask

def normalize_signal(signal):
    max_amplitude = np.max(np.abs(signal))
    if max_amplitude == 0:
        return signal
    scale = 32767 / max_amplitude
    return (signal * scale).astype(np.int16)

def write_wav(filename, signal, sample_rate):
    signal = normalize_signal(signal)
    with open(filename, "wb") as f:
        f.write(b'RIFF')
        f.write((36 + len(signal) * 2).to_bytes(4, byteorder='little'))
        f.write(b'WAVEfmt ')
        f.write((16).to_bytes(4, byteorder='little'))
        f.write((1).to_bytes(2, byteorder='little'))
        f.write((1).to_bytes(2, byteorder='little'))
        f.write(sample_rate.to_bytes(4, byteorder='little'))
        f.write((sample_rate * 2).to_bytes(4, byteorder='little'))
        f.write((2).to_bytes(2, byteorder='little'))
        f.write((16).to_bytes(2, byteorder='little'))
        f.write(b'data')
        f.write((len(signal) * 2).to_bytes(4, byteorder='little'))
        f.write(signal.tobytes())

def process_block(i, samples, block_size, sample_rate):
    end = min(i + block_size, len(samples))  # Éviter un dépassement
    block = samples[i:end]
    magnitude, phase = dft(block)
    amplified_magnitude = amplify(magnitude, 2)  # Amplification sans distorsion
    # filtered_spectrum = noise_reduction(amplified_magnitude, 100, 5000, sample_rate)
    processed_block = idft(amplified_magnitude, phase)
    return processed_block[:len(block)]

if __name__ == "__main__":
    sample_rate, samples = read_wav("audio_bruite.wav")
    processed_signal = np.zeros_like(samples, dtype=np.int16)
    block_size = 4096  # Traitement par blocs

    for i in range(0, len(samples), block_size):
        processed_block = process_block(i, samples, block_size, sample_rate)
        end = min(i + block_size, len(samples))
        processed_signal[i:end] = processed_block[:end - i]

    write_wav("output_processed.wav", processed_signal, sample_rate)
    print("Audio traité et sauvegardé ! ✅")
