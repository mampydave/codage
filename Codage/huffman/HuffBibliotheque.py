import huffman

# Texte à compresser
text = "abracadabra"

# Compression Huffman
encoded_text, huffman_tree = huffman.codebook(text)

# Encodage du texte
compressed = "".join(encoded_text[char] for char in text)

# Décodage du texte
decoded_text = huffman.decompress(compressed, huffman_tree)

print("Texte original :", text)
print("Texte encodé :", compressed)
print("Texte décodé :", decoded_text)
