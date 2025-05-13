import wave
import numpy as np
import struct

def safe_lsb_modification(sample, bit_value, sample_width):
    """Modifie le LSB en garantissant que la valeur reste dans les limites"""
    if sample_width == 1:  
        return np.uint8((sample & 0xFE) | bit_value)
    elif sample_width == 2:  
        new_val = (int(sample) & 0xFFFE) | bit_value
        if new_val > 32767:
            new_val -= 65536
        return np.int16(new_val)
    elif sample_width == 3:  
        return sample
    elif sample_width == 4:  
        return np.int32((sample & 0xFFFFFFFE) | bit_value)
    else:
        raise ValueError("Taille d'échantillon non supportée")

def encoder_audio(audio_path, message_binaire, output_path):
    """Version finale avec gestion des tableaux en écriture"""
    with wave.open(audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = audio.readframes(audio.getnframes())
    
    sample_width = params.sampwidth
    n_channels = params.nchannels
    total_samples = len(frames) // sample_width
    
    # Création d'une copie modifiable des frames
    frames_copy = bytearray(frames)
    
    if sample_width == 1:
        dtype = np.uint8
    elif sample_width == 2:
        dtype = np.int16
    elif sample_width == 3:
        # Traitement spécial 24-bit
        frames_24bit = np.frombuffer(frames_copy, dtype=np.uint8)
    elif sample_width == 4:
        dtype = np.int32
    else:
        raise ValueError("Format non supporté")

    if sample_width != 3:
        # Création d'un tableau modifiable
        audio_array = np.frombuffer(frames_copy, dtype=dtype).copy()
    
    # Vérification capacité
    available_bits = total_samples * n_channels
    if len(message_binaire) > available_bits:
        raise ValueError(f"Message trop long. Capacité: {available_bits} bits")

    modified_indices = []
    for i in range(len(message_binaire)):
        byte_pos = i * sample_width
        
        if sample_width == 3:
            frames_copy[byte_pos + 2] = (frames_copy[byte_pos + 2] & 0xFE) | int(message_binaire[i])
        else:
            original = int.from_bytes(frames_copy[byte_pos:byte_pos+sample_width], 
                                    'little', 
                                    signed=(sample_width > 1))
            
            modified = safe_lsb_modification(original, int(message_binaire[i]), sample_width)
            
            frames_copy[byte_pos:byte_pos+sample_width] = modified.tobytes()
        
        modified_indices.append(i)

    with wave.open(output_path, 'wb') as output:
        output.setparams(params)
        output.writeframes(frames_copy)
    
    return modified_indices

def decoder_audio(audio_path, indices):
    """Décodeur utilisant les indices linéaires"""
    with wave.open(audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = audio.readframes(audio.getnframes())
    
    sample_width = params.sampwidth
    message = []
    
    for idx in indices:
        byte_pos = idx * sample_width
        
        if sample_width == 1:
            sample = frames[byte_pos]
        elif sample_width == 2:
            sample = int.from_bytes(frames[byte_pos:byte_pos+2], 'little', signed=True)
        elif sample_width == 3:
            sample = frames[byte_pos + 2]
        elif sample_width == 4:
            sample = int.from_bytes(frames[byte_pos:byte_pos+4], 'little', signed=True)
        
        message.append(str(sample & 1))
    
    return ''.join(message)

if __name__ == "__main__":
    try:
        message = "100101110010000100111001"
        # print(f"Message original: {message}")
        
        # Encodage
        # indices = encoder_audio("440.wav", message, "output.wav")
        # print(f"Indices modifiés: {indices}")
        
        # Décodage
        indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        decoded = decoder_audio("output.wav", indices)
        print(f"Message décodé: {decoded}")
        print(f"Correspondance: {message == decoded}")

    except Exception as e:
        print(f"Erreur: {e}")