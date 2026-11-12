# Lekcja 06 - Zadanie 2: Bezpieczny dostęp do słownika

# Konfiguracja modelu
konfig = {
    'lr': 0.01,
    'epochs': 100,
    'optimizer': 'adam'
}

# Pobranie wartości istniejącego klucza
lr = konfig.get('lr')

# Pobranie wartości nieistniejącego klucza
momentum = konfig.get('momentum')

# Pobranie wartości z wartością domyślną
momentum_domyslne = konfig.get('momentum', 0.9)

# Sprawdzenie obecności klucza
czy_batch_size = 'batch_size' in konfig

# Wyświetlanie wyników
print(f"Learning rate: {lr}")
print(f"Momentum: {momentum}")
print(f"Momentum domyślne: {momentum_domyslne}")
print(f"Czy batch_size istnieje: {czy_batch_size}")
