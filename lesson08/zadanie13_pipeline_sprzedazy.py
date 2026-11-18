# Lekcja 08 - Zadanie 13: Pipeline przetwarzania danych sprzedazowych

# Dane wejsciowe
sprzedaz = [
    (1, "elektronika", 45, 12500),
    (1, "odziez", 78, 4200),
    (2, "elektronika", 52, 15200),
    (2, "odziez", 65, 3800),
    (3, "elektronika", 38, 9800),
    (3, "odziez", 82, 5100),
    (4, "elektronika", 61, 18900),
    (4, "odziez", 71, 4500)
]


# 1. Konwersja krotki na slownik
def tuple_to_dict(rekord):
    dzien, kategoria, liczba_transakcji, wartosc = rekord

    return {
        "dzien": dzien,
        "kategoria": kategoria,
        "liczba_transakcji": liczba_transakcji,
        "wartosc": wartosc
    }


# 2. Feature engineering
def dodaj_srednia_transakcji(rekord):
    srednia = rekord["wartosc"] / rekord["liczba_transakcji"]

    return {
        **rekord,
        "srednia_transakcji": round(srednia, 2)
    }


# 3. Agregacja wedlug kategorii
def agreguj_po_kategorii(dane):
    agregacja = {}

    for rekord in dane:
        kategoria = rekord["kategoria"]
        wartosc = rekord["wartosc"]

        agregacja[kategoria] = (
            agregacja.get(kategoria, 0) + wartosc
        )

    return agregacja


# PIPELINE PRZETWARZANIA DANYCH

# Etap 1 - konwersja danych
dane = [tuple_to_dict(rekord) for rekord in sprzedaz]

# Etap 2 - dodanie nowej cechy
dane_rozszerzone = [
    dodaj_srednia_transakcji(rekord)
    for rekord in dane
]

# Etap 3 - agregacja
agregacja = agreguj_po_kategorii(dane_rozszerzone)

# Etap 4 - sortowanie malejaco
ranking = sorted(
    agregacja.items(),
    key=lambda x: x[1],
    reverse=True
)

# Wyswietlenie danych po przetworzeniu
print("PIPELINE PRZETWARZANIA DANYCH SPRZEDAZOWYCH")
print("=" * 75)

print("\nDANE PO FEATURE ENGINEERING")
print("-" * 75)

print(
    f"{'Dzien':>5} {'Kategoria':>15} "
    f"{'Transakcje':>12} {'Wartosc':>12} "
    f"{'Srednia':>12}"
)

for rekord in dane_rozszerzone:
    print(
        f"{rekord['dzien']:>5} "
        f"{rekord['kategoria']:>15} "
        f"{rekord['liczba_transakcji']:>12} "
        f"{rekord['wartosc']:>12.2f} "
        f"{rekord['srednia_transakcji']:>12.2f}"
    )

# Ranking kategorii
print("\nRANKING KATEGORII")
print("=" * 75)

for miejsce, (kategoria, wartosc) in enumerate(ranking, 1):
    print(f"{miejsce}. {kategoria:15} {wartosc:10.2f} zl")

# Podsumowanie
print("\nPODSUMOWANIE")
print("=" * 75)

print(f"Liczba rekordow: {len(dane_rozszerzone)}")
print(f"Liczba kategorii: {len(agregacja)}")
print(f"Laczna liczba transakcji: {sum(r['liczba_transakcji'] for r in dane)}")
print(f"Laczna wartosc sprzedazy: {sum(agregacja.values()):.2f} zl")

# Weryfikacja
oczekiwane = {"elektronika": 56400, "odziez": 17600}

print(f"Czy wynik jest poprawny: {agregacja == oczekiwane}")
