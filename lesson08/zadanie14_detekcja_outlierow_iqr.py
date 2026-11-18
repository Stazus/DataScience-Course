# Lekcja 08 - Zadanie 14: Detekcja outlierow metoda IQR

# Dane wejsciowe
czasy_odpowiedzi = [
    120, 135, 142, 128, 5000, 138,
    145, 119, 10000, 133, 141
]


# Funkcja wykrywajaca wartosci odstajace
def wykryj_outliery(dane):
    """Zwraca czyste dane i outliery metoda IQR."""

    # Sortowanie danych
    posortowane = sorted(dane)
    n = len(posortowane)

    # Obliczenie kwartylow
    q1 = posortowane[n // 4]
    q3 = posortowane[3 * n // 4]

    # Rozstep miedzykwartylowy
    iqr = q3 - q1

    # Wyznaczenie granic
    dolna_granica = q1 - 1.5 * iqr
    gorna_granica = q3 + 1.5 * iqr

    # Filtrowanie danych - list comprehensions
    czyste_dane = [
        x for x in dane
        if dolna_granica <= x <= gorna_granica
    ]

    outliery = [
        x for x in dane
        if x < dolna_granica or x > gorna_granica
    ]

    # Wyswietlenie parametrow IQR
    print(f"Dane posortowane: {posortowane}")
    print(f"Q1: {q1}")
    print(f"Q3: {q3}")
    print(f"IQR: {iqr}")
    print(f"Dolna granica: {dolna_granica}")
    print(f"Gorna granica: {gorna_granica}")

    return czyste_dane, outliery


# Wywolanie funkcji
print("DETEKCJA OUTLIEROW - METODA IQR")
print("=" * 60)

print(f"Dane oryginalne: {czasy_odpowiedzi}\n")

czyste_dane, outliery = wykryj_outliery(czasy_odpowiedzi)

# Wyswietlenie wynikow
print("\nWYNIKI")
print("=" * 60)

print(f"Czyste dane: {czyste_dane}")
print(f"Outliery: {outliery}")

print(f"\nLiczba wszystkich danych: {len(czasy_odpowiedzi)}")
print(f"Liczba czystych danych: {len(czyste_dane)}")
print(f"Liczba outlierow: {len(outliery)}")

# Weryfikacja wyniku
oczekiwane = [5000, 10000]

print(f"Czy wynik jest poprawny: {outliery == oczekiwane}")
