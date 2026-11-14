# Lekcja 06 - Zadanie 17: Diagnoza roznic miedzy wersjami konfiguracji

# Pierwsza wersja konfiguracji
wersja_1 = {
    'lr': 0.01,
    'epochs': 100,
    'optimizer': 'sgd',
    'batch_size': 32,
    'dropout': 0.2
}

# Druga wersja konfiguracji
wersja_2 = {
    'lr': 0.001,
    'epochs': 100,
    'optimizer': 'adam',
    'batch_size': 64,
    'momentum': 0.9
}

# Zbiory kluczy obu konfiguracji
klucze_1 = set(wersja_1)
klucze_2 = set(wersja_2)

# Operacje na zbiorach
wszystkie = klucze_1 | klucze_2
wspolne = klucze_1 & klucze_2
tylko_1 = klucze_1 - klucze_2
tylko_2 = klucze_2 - klucze_1

# Raport dotyczacy kluczy
print("POROWNANIE KONFIGURACJI")
print("=" * 50)
print(f"Wszystkie klucze: {wszystkie}")
print(f"Klucze wspolne: {wspolne}")
print(f"Klucze tylko w wersji 1: {tylko_1}")
print(f"Klucze tylko w wersji 2: {tylko_2}")

# Porownanie wartosci wspolnych parametrow
rozne_lr = wersja_1['lr'] != wersja_2['lr']
rozne_epochs = wersja_1['epochs'] != wersja_2['epochs']
rozne_optimizer = wersja_1['optimizer'] != wersja_2['optimizer']
rozne_batch_size = wersja_1['batch_size'] != wersja_2['batch_size']

# Wyswietlenie flag True/False
print("\nROZNICE W WARTOSCIACH")
print("=" * 50)
print(f"lr: {rozne_lr}")
print(f"epochs: {rozne_epochs}")
print(f"optimizer: {rozne_optimizer}")
print(f"batch_size: {rozne_batch_size}")
