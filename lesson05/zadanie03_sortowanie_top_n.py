# Lekcja 05 - Zadanie 3: Sortowanie listy i top-N

# Wyniki accuracy modeli
wyniki = [0.78, 0.92, 0.85, 0.88, 0.81, 0.95, 0.79]

# Sortowanie malejące
wyniki.sort(reverse=True)

# Wybór trzech najlepszych wyników
top_3 = wyniki[:3]

# Wyświetlanie wyników
print(f"Wyniki posortowane malejąco: {wyniki}")
print(f"Trzy najlepsze wyniki: {top_3}")
