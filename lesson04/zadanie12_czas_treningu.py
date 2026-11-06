# Lekcja 04 - Zadanie 12: Estymacja czasu treningu

liczba_probek = 50000
batch_size = 128
epochs = 50
czas_batcha = 0.15

# Obliczenie liczby batchy na epokę
pelne_batche = liczba_probek // batch_size
reszta = liczba_probek % batch_size

batche_na_epoke = pelne_batche + (1 if reszta > 0 else 0)

# Obliczenie całkowitego czasu treningu
czas_calkowity = batche_na_epoke * epochs * czas_batcha

# Konwersja na godziny, minuty i sekundy
godziny = int(czas_calkowity // 3600)
minuty = int((czas_calkowity % 3600) // 60)
sekundy = czas_calkowity % 60

# Wyświetlenie wyników
print(f"Liczba pełnych batchy: {pelne_batche}")
print(f"Pozostałe próbki: {reszta}")
print(f"Batchy na epokę: {batche_na_epoke}")
print(f"Całkowity czas: {czas_calkowity:.1f} s")

print(f"Szacowany czas: {godziny} h {minuty} min {sekundy:g} s")
