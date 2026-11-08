# Lekcja 05 - Zadanie 2: Dodawanie elementów do listy

# Utworzenie pustej listy
results = []

# Dodawanie wyników accuracy
results.append(0.75)
results.append(0.82)
results.append(0.79)
results.append(0.85)
results.append(0.88)

# Obliczanie statystyk
liczba_wynikow = len(results)
srednia = sum(results) / liczba_wynikow
maksimum = max(results)
minimum = min(results)

# Wyświetlanie wyników
print(f"Wyniki accuracy: {results}")
print(f"Liczba wyników: {liczba_wynikow}")
print(f"Średnia accuracy: {srednia:.3f}")
print(f"Maksymalna accuracy: {maksimum:.2f}")
print(f"Minimalna accuracy: {minimum:.2f}")
