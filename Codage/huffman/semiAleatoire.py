import random

observed_pairs = [(2, 2), (4, 4), (6, 6), (8, 8)]
found_seed = None

for seed in range(10000):  # Limité pour l'exemple
    random.seed(seed)
    match = True
    for (x_real, y_real) in observed_pairs:
        # x_pred = random.randint(0, 100)
        # y_pred = random.randint(0, 100)
        x_pred = random.randrange(0, 10, 2)
        y_pred = random.randrange(0, 10, 2)
        if (x_pred, y_pred) != (x_real, y_real):
            match = False
            break
    if match:
        found_seed = seed
        break

print("Seed trouvée :", found_seed)

random.seed(found_seed)  # Initialisation avec une graine fixe
for _ in range(10):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    print(f"({x}, {y})")
