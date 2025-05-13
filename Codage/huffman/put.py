from PIL import Image
import numpy as np

def encoder_message(image_path, message_binaire, output_path):
    """Encode un message binaire dans les LSB du canal R d'une image"""
    # Ouvrir l'image
    img = Image.open(image_path)
    pixels = np.array(img)
    width = img.width
    
    # Vérifier si l'image a un canal alpha (RGBA)
    has_alpha = img.mode == 'RGBA'
    
    if len(message_binaire) > img.width * img.height:
        raise ValueError("Message trop long pour l'image")
    
    positions_modifiees = []
    index_message = 0
    
    for y in range(img.height):
        for x in range(img.width):
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
            
            positions_modifiees.append(y * width + x)
            index_message += 1
    
    # Sauvegarder l'image modifiée
    Image.fromarray(pixels).save(output_path)
    return positions_modifiees

# Paramètres
message = "100101110010000100111001"
image_input = "coder.png"
image_output = "image_modifiee.png"

# Encoder le message
positions = encoder_message(image_input, message, image_output)
print(f"Indices des pixels modifiés: {positions}")