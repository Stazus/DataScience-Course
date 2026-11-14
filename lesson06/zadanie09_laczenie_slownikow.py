# Lekcja 06 - Zadanie 9: Konfiguracja modelu - laczenie slownikow

# Domyslna konfiguracja modelu
domyslne = {
    'lr': 0.01,
    'epochs': 100,
    'optimizer': 'sgd',
    'batch_size': 32
}

# Konfiguracja uzytkownika
uzytkownika = {
    'lr': 0.001,
    'batch_size': 64,
    'momentum': 0.9
}

# Laczenie slownikow operatorem |
finalna_1 = domyslne | uzytkownika

# Laczenie slownikow metoda update()
finalna_2 = domyslne.copy()
finalna_2.update(uzytkownika)

# Porownanie konfiguracji
czy_rowne = finalna_1 == finalna_2

# Wyswietlanie wynikow
print(f"Konfiguracja domyslna: {domyslne}")
print(f"Konfiguracja uzytkownika: {uzytkownika}")
print(f"\nKonfiguracja przez |: {finalna_1}")
print(f"Konfiguracja przez update(): {finalna_2}")
print(f"\nCzy konfiguracje sa rowne: {czy_rowne}")

# Wyswietlenie wybranych parametrow
print("\nFINALNA KONFIGURACJA")
print(
    f"lr: {finalna_1['lr']}\n"
    f"batch_size: {finalna_1['batch_size']}\n"
    f"momentum: {finalna_1['momentum']}"
)
