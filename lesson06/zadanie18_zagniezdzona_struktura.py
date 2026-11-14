# Lekcja 06 - Zadanie 18: Maly JSON - zagniezdzona struktura

# Konfiguracja eksperymentu Machine Learning
projekt = {
    'nazwa': 'iris_classification',
    'wersja': (1, 2, 0),
    'autorzy': {'Anna', 'Bartek', 'Cezary'},
    'dataset': {
        'nazwa': 'Iris',
        'shape': (150, 4),
        'klasy': ('setosa', 'versicolor', 'virginica')
    },
    'hiperparametry': {
        'lr': 0.001,
        'batch_size': 64,
        'epochs': 50
    }
}

# 1. Rozpakowanie wersji projektu
major, minor, patch = projekt['wersja']

print("KONFIGURACJA PROJEKTU")
print("=" * 50)
print(f"Projekt: {projekt['nazwa']}")
print(f"Wersja: v{major}.{minor}.{patch}")

# 2. Rozpakowanie wymiarow datasetu
n_rekordow, n_cech = projekt['dataset']['shape']

print(f"Dataset {projekt['dataset']['nazwa']}: {n_rekordow} x {n_cech}")

# 3. Dodanie nowego autora
projekt['autorzy'].add('Dorota')

# 4. Liczba i posortowana lista autorow
print("\nAUTORZY PROJEKTU")
print(f"Liczba autorow: {len(projekt['autorzy'])}")
print(f"Autorzy: {sorted(projekt['autorzy'])}")

# 5. Aktualizacja hiperparametrow
projekt['hiperparametry'].update({
    'dropout': 0.3,
    'batch_size': 128
})

print("\nHIPERPARAMETRY")
print(projekt['hiperparametry'])

# 6. Zamiana krotki klas na zbior
projekt['dataset']['klasy'] = set(projekt['dataset']['klasy'])

czy_setosa = 'setosa' in projekt['dataset']['klasy']

print("\nKLASY DATASETU")
print(f"Klasy: {projekt['dataset']['klasy']}")
print(f"Czy setosa jest w zbiorze: {czy_setosa}")
