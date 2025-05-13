from PIL import Image

def extraire_lsb_pixels(image_path, pixels_list, verbose=False):
    """
    Version améliorée avec vérifications et mode debug
    """
    try:
        img = Image.open(image_path)
        if verbose:
            print(f"Format: {img.format}, Mode: {img.mode}, Taille: {img.size}")
        
        width, height = img.size
        total_pixels = width * height
        pixels = img.load()
        lsb_bits = []
        
        for i, pos in enumerate(pixels_list):
            if pos >= total_pixels:
                if verbose:
                    print(f"Position {i} (index {pos}) hors limites")
                continue
            
            x = pos % width
            y = pos // width

            r, g, b = pixels[x, y][:3]
            lsb_r = r & 1
            lsb_g = g & 1
            lsb_b = b & 1
            
            if verbose:
                print(f"Pixel {i} ({x},{y}) - R:{r}→{lsb_r}, G:{g}→{lsb_g}, B:{b}→{lsb_b}")
            
            # lsb_bits.extend([str(lsb_r), str(lsb_g), str(lsb_b)])
            lsb_bits.extend([str(lsb_r)])
        
        result = ''.join(lsb_bits)
        if verbose:
            print(f"Résultat brut: {result}")
            print(f"Nombre de bits extraits: {len(result)}")
            print(f"Nombre de 1 trouvés: {result.count('1')}/{len(result)}")
        
        return result

    except Exception as e:
        print(f"Erreur: {e}")
        return ""

pixels_cibles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
bits_lsb = extraire_lsb_pixels("image_modifiee.png", pixels_cibles, verbose = True)
print("LSB extraits:", bits_lsb)

# img_test = Image.new("RGB", (10, 10), color=(125, 254, 13))  # R=125(1), G=254(0), B=13(1)
# img_test.save("test_lsb.png")
# bits = extraire_lsb_pixels("test_lsb.png", [(0,0), (5,5),(9,9)], verbose=True)
# print("LSB extraits:", bits)
