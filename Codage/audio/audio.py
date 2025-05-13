import math
import struct

def read_wav(filename):
    with open(filename, "rb") as f:
        header = f.read(44)
        sample_rate = int.from_bytes(header[24:28], byteorder="little")
        data = f.read()
    
    signal = [struct.unpack('<h', data[i:i+2])[0] for i in range(0, len(data), 2)]
    return sample_rate, signal

def dft(signal):
    N = len(signal)
    magnitude = [0] * N
    phase = [0] * N
    
    for k in range(N):
        real = sum(signal[n] * math.cos(-2 * math.pi * k * n / N) for n in range(N))
        imag = sum(signal[n] * math.sin(-2 * math.pi * k * n / N) for n in range(N))
        magnitude[k] = math.sqrt(real**2 + imag**2)
        phase[k] = math.atan2(imag, real)
    
    return magnitude, phase

def amplify(spectrum, gain):
    return [x * gain for x in spectrum]

def noise_reduction(spectrum, low_cutoff, high_cutoff, sample_rate):
    N = len(spectrum)
    freqs = [i * sample_rate / N for i in range(N)]
    
    return [spectrum[i] if low_cutoff <= freqs[i] <= high_cutoff else 0 for i in range(N)]

def reduce_distortion(spectrum, threshold=0.2):
    avg_amplitude = sum(spectrum) / len(spectrum)
    return [x * 0.8 if x > avg_amplitude * (1 + threshold) else x for x in spectrum]

def idft(magnitude, phase):
    N = len(magnitude)
    signal = [
        sum(magnitude[k] * math.cos(2 * math.pi * k * n / N + phase[k]) for k in range(N))
        for n in range(N)
    ]
    return signal

def normalize_signal(signal):
    max_amplitude = max(abs(sample) for sample in signal)
    if max_amplitude == 0:
        return signal
    scale = 32767 / max_amplitude
    return [int(sample * scale) for sample in signal]

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
        
        for sample in signal:
            f.write(struct.pack('<h', sample))

def process_audio_in_blocks(samples, sample_rate, block_size=1024):
    processed_signal = []
    num_blocks = len(samples) // block_size
    
    for i in range(num_blocks):
        block = samples[i * block_size:(i + 1) * block_size]
        spectrum, phase = dft(block)
        spectrum = amplify(spectrum, 1.5)
        spectrum = noise_reduction(spectrum, 100, 5000, sample_rate)
        spectrum = reduce_distortion(spectrum)
        processed_block = idft(spectrum, phase)
        processed_signal.extend(processed_block)
        print(f"Processing block {i + 1}/{num_blocks}...")
    
    return processed_signal

if __name__ == "__main__":
    sample_rate, samples = read_wav("440.wav")
    processed_signal = process_audio_in_blocks(samples, sample_rate)
    write_wav("output_processed.wav", processed_signal, sample_rate)
    print("Audio traité et sauvegardé ! ✅")
