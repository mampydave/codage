import numpy as np
from PIL import Image
import random

def encoder_message(image_path, message_binaire, output_path, seed=None):
    """Encode un message binaire dans les LSB du canal R d'une image de manière aléatoire"""
    # Ouvrir l'image
    img = Image.open(image_path)
    pixels = np.array(img)
    
    # Vérifier si l'image a un canal alpha (RGBA)
    has_alpha = img.mode == 'RGBA'
    
    if len(message_binaire) > img.width * img.height:
        raise ValueError("Message trop long pour l'image")
    
    # Initialiser le générateur aléatoire avec une graine (optionnelle)
    if seed is not None:
        random.seed(seed)
    
    # Créer une liste de toutes les positions possibles
    positions = [(x, y) for y in range(img.height) for x in range(img.width)]
    
    # Mélanger aléatoirement les positions
    random.shuffle(positions)
    
    positions_modifiees = []
    index_message = 0
    
    for x, y in positions:
        if index_message >= len(message_binaire):
            break
        
        # Gérer différemment RGBA vs RGB
        if has_alpha:
            r, g, b, a = pixels[y, x]
            nouveau_r = (r & 0xFE) | int(message_binaire[index_message])
            pixels[y, x] = (nouveau_r, g, b, a)
        else:
            r, g, b = pixels[y, x]
            nouveau_r = (r & 0xFE) | int(message_binaire[index_message])
            pixels[y, x] = (nouveau_r, g, b)
        
        positions_modifiees.append((x, y))
        index_message += 1
    
    # Sauvegarder l'image modifiée
    Image.fromarray(pixels).save(output_path)
    return positions_modifiees

message = "100101110010000100111001"
image_input = "coder.png"
image_output = "image_modifiee.png"

# Encoder le message
positions = encoder_message(image_input, message, image_output,18)
print(f"Positions des pixels modifiés (x,y): {positions}")    