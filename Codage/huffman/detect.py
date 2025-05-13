from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def detect_lsb_anomalies(image_path, threshold=0.1):
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)
    
    # Extraire tous les LSB
    lsb = pixels[:,:,:] & 1
    
    # Calculer la proportion de 1 par canal
    prop_r = np.mean(lsb[:,:,0])
    prop_g = np.mean(lsb[:,:,1])
    prop_b = np.mean(lsb[:,:,2])
    
    print(f"Proportion de LSB=1 → R: {prop_r:.3f}, G: {prop_g:.3f}, B: {prop_b:.3f}")
    
    # Identifier les canaux suspects (proportion éloignée de 0.5)
    suspicious_channels = []
    if abs(prop_r - 0.5) > threshold:
        suspicious_channels.append('R')
    if abs(prop_g - 0.5) > threshold:
        suspicious_channels.append('G')
    if abs(prop_b - 0.5) > threshold:
        suspicious_channels.append('B')
    
    return suspicious_channels


def find_modified_pixels(image_path, channel='R'):
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)
    
    modified_positions = []
    for y in range(img.height):
        for x in range(img.width):
            if (pixels[y,x][['R','G','B'].index(channel)] & 1) == 1:
                modified_positions.append((x, y))
    
    return modified_positions[:1000]  # Retourne les 1000 premiers pour éviter des listes énormes


def highlight_modified_pixels(image_path, channel='R'):
    img = Image.open(image_path)
    pixels = np.array(img.convert("RGB"))
    
    # Créer un masque des LSB=1
    lsb_mask = (pixels[:,:,['R','G','B'].index(channel)] & 1) * 255
    
    plt.imshow(lsb_mask, cmap='gray')
    plt.title(f"Pixels modifiés (LSB=1) dans le canal {channel}")
    plt.show()

suspicious_channels = detect_lsb_anomalies("image_modifiee.png")
print(f"Canaux suspects : {suspicious_channels}")

modified_pixels = find_modified_pixels("image_modifiee.png", channel='R')
print(f"Premiers pixels modifiés : {modified_pixels[:10]}")

highlight_modified_pixels("image_modifiee.png", channel='R')