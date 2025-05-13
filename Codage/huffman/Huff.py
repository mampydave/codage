import heapq
from collections import Counter, namedtuple

# Définition de la classe pour un nœud de l'arbre de Huffman
class HuffmanNode(namedtuple("HuffmanNode", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq  # Comparaison basée sur la fréquence

# Construction de l'arbre de Huffman
def build_huffman_tree(frequency_map):
    heap = [HuffmanNode(char, freq, None, None) for char, freq in frequency_map.items()]
    heapq.heapify(heap)  # Crée une min-heap

    while len(heap) > 1:
        left = heapq.heappop(heap)  # Extraire le nœud avec la plus petite fréquence
        right = heapq.heappop(heap)  # Extraire le second plus petit
        merged = HuffmanNode(None, left.freq + right.freq, left, right)  # Fusionner
        heapq.heappush(heap, merged)  # Ajouter le nouveau nœud à la heap

    return heap[0]  # Retourne la racine de l'arbre

# Génération des codes Huffman
def generate_huffman_codes(node, code="", huffman_codes={}):
    if node:
        if node.char is not None:  # Feuille atteinte
            huffman_codes[node.char] = code or "0"  # Assigner un code au caractère
        generate_huffman_codes(node.left, code + "0", huffman_codes)
        generate_huffman_codes(node.right, code + "1", huffman_codes)
    return huffman_codes

# Encodage d'un texte avec Huffman
def huffman_encode(text):
    frequency_map = Counter(text)  # Compte la fréquence de chaque caractère
    root = build_huffman_tree(frequency_map)  # Construction de l'arbre
    huffman_codes = generate_huffman_codes(root)  # Génération des codes
    
    encoded_text = "".join(huffman_codes[char] for char in text)  # Encodage du texte
    return encoded_text, huffman_codes, root

# Décodage d'un texte compressé
def huffman_decode(encoded_text, root):
    decoded_text = []
    node = root
    for bit in encoded_text:
        node = node.left if bit == "0" else node.right
        if node.char is not None:  # Feuille atteinte
            decoded_text.append(node.char)
            node = root  # Retour à la racine
    return "".join(decoded_text)

# Exemple d'utilisation
if __name__ == "__main__":
    text = "abracadabra"
    
    # Encodage
    encoded_text, huffman_codes, root = huffman_encode(text)
    print("Texte original :", text)
    print("Codes Huffman :", huffman_codes)
    print("Texte encodé :", encoded_text)
    
    # Décodage
    decoded_text = huffman_decode(encoded_text, root)
    print("Texte décodé :", decoded_text)
