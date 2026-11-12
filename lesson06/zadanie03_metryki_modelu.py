# Lekcja 06 - Zadanie 3: Metryki modelu

# Słownik metryk modelu
metryki = {
    'accuracy': 0.94,
    'precision': 0.91,
    'recall': 0.89,
    'f1_score': 0.90
}

# Najwyższa i najniższa wartość metryki
maksimum = max(metryki.values())
minimum = min(metryki.values())

# Obliczenie średniej
srednia = sum(metryki.values()) / len(metryki)

# Sortowanie kluczy alfabetycznie
klucze_posortowane = sorted(metryki.keys())

# Sortowanie wartości rosnąco
wartosci_posortowane = sorted(metryki.values())

# Wyświetlanie wyników
print(f"Metryki modelu: {metryki}")
print(f"Najwyższa metryka: {maksimum:.2f}")
print(f"Najniższa metryka: {minimum:.2f}")
print(f"Średnia metryka: {srednia:.3f}")
print(f"Posortowane klucze: {klucze_posortowane}")
print(f"Posortowane wartości: {wartosci_posortowane}")
