import numpy as np
from typing import List, Tuple
import random

def generer_positions_aleatoires(
    largeur: int, 
    hauteur: int, 
    seed: int = None, 
    taille_message: int = None
) -> List[Tuple[int, int]]:
    """
    Génère une séquence pseudo-aléatoire de positions (x,y) pour cacher un message.
    
    Args:
        largeur (int): Largeur de l'image
        hauteur (int): Hauteur de l'image
        seed (int, optional): Graine pour la reproductibilité. Defaults to None.
        taille_message (int, optional): Nombre de positions nécessaires. Si None, toutes les positions.
    
    Returns:
        List[Tuple[int, int]]: Liste de positions (x,y) mélangées aléatoirement
    """
    # Créer un tableau de toutes les positions possibles
    positions = [(x, y) for y in range(hauteur) for x in range(largeur)]
    
    # Initialiser le générateur aléatoire
    rng = np.random.RandomState(seed)
    
    # Mélanger les positions
    indices = np.arange(len(positions))
    rng.shuffle(indices)
    
    # Sélectionner seulement le nombre nécessaire de positions
    if taille_message is not None:
        indices = indices[:taille_message]
    
    # Retourner les positions dans l'ordre mélangé
    return [positions[i] for i in indices]


positions = generer_positions_aleatoires(105, 70, seed=18, taille_message=24)
print(f"Positions des pixels modifiés (x,y): {positions}")    
