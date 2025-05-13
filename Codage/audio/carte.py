import random

def generate_code(prefix):
    """ Génère un code de recharge de 14 chiffres avec un préfixe placé aléatoirement. """

    if not prefix.isdigit() or len(prefix) != 4:
        raise ValueError("Le préfixe doit contenir exactement 4 chiffres.")

    # Générer les chiffres restants (9 chiffres aléatoires)
    remaining_digits = [random.randint(0, 9) for _ in range(9)]

    # Choisir une position aléatoire pour insérer le préfixe (0 à 9)
    pos = random.randint(0, 9)

    # Construire la séquence avant d'ajouter le chiffre de contrôle
    code_base = remaining_digits[:pos] + [int(d) for d in prefix] + remaining_digits[pos:]

    # Calcul du chiffre de contrôle (Luhn)
    def luhn_checksum(digits):
        total = 0
        reverse_digits = digits[::-1]
        for i, num in enumerate(reverse_digits):
            if i % 2 == 0:
                num *= 2
                if num > 9:
                    num -= 9
            total += num
        return (10 - (total % 10)) % 10

    check_digit = luhn_checksum(code_base)

    # Ajouter le chiffre de contrôle
    code_base.append(check_digit)

    return ''.join(map(str, code_base))

# Génération de codes pour chaque opérateur à Madagascar
madagascar_prefixes = {
    "Orange": "4201",
    "Telma": "3134",
    "Airtel": "5547",
    "Bip": "6678"
}

codes = {op: generate_code(prefix) for op, prefix in madagascar_prefixes.items()}

for operator, code in codes.items():
    print(f"{operator}: {code}")
