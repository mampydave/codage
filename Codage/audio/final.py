import numpy as np

def read_wav(filename):
    with open(filename, "rb") as f:
        header = f.read(44)
        sample_rate = int.from_bytes(header[24:28], byteorder="little")
        data = np.frombuffer(f.read(), dtype=np.int16)
    return sample_rate, data

def dft(signal):
    # Calcul de la transformée de Fourier (DFT) avec FFT
    spectrum = np.fft.fft(signal)
    magnitude = np.abs(spectrum)
    phase = np.angle(spectrum)
    return magnitude, phase, spectrum

def idft(magnitude, phase):
    # Calcul de l'IDFT avec IFFT
    spectrum = magnitude * np.exp(1j * phase)  # Recombiner magnitude et phase
    return np.fft.ifft(spectrum).real.astype(np.int16)

def amplify(magnitude, gain):
    # Amplification des magnitudes
    return magnitude * gain
    
def normalize_signal(signal):
    max_amplitude = np.max(np.abs(signal))
    if max_amplitude == 0:
        return signal
    scale = 32767 / max_amplitude  # Normaliser à 16 bits
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
    block = samples[i:i + block_size]
    magnitude, phase, spectrum = dft(block)  # Calcul de la DFT
    amplified_magnitude = amplify(magnitude, 1.1)  # Réduction du gain pour éviter l'amplification excessive
    
    processed_block = amplified_magnitude  # Signal filtré avec bruit réduit
    return processed_block[:len(block)]

if __name__ == "__main__":
    sample_rate, samples = read_wav("audio_bruite.wav")
    processed_signal = np.zeros_like(samples, dtype=np.int16)
    block_size = 4096  # Traitement par blocs

    # Traitement des blocs
    for i in range(0, len(samples), block_size):
        processed_block = process_block(i, samples, block_size, sample_rate)
        processed_signal[i:i + block_size] = processed_block
        print(f"Processing block {i + 1}/{len(samples)}...")

    write_wav("output_processed.wav", processed_signal, sample_rate)
    print("Audio traité et sauvegardé ! ✅")
