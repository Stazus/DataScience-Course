# Lekcja 08 - Zadanie 19: Pipeline - czyszczenie, normalizacja, segmentacja

# Dane wejsciowe
klienci = [
    {"id": 1, "wiek": 25, "dochod": 4500, "wydatki": 3200},
    {"id": 2, "wiek": 200, "dochod": 7800, "wydatki": 5100},
    {"id": 3, "wiek": 45, "dochod": 9200, "wydatki": -500},
    {"id": 4, "wiek": 30, "dochod": 6000, "wydatki": 4000},
    {"id": 5, "wiek": 50, "dochod": 11000, "wydatki": 6500},
    {"id": 6, "wiek": 28, "dochod": 5000, "wydatki": 3500}
]


# 1. Czyszczenie danych
def usun_outliery(klienci):
    """Usuwa rekordy z nieprawidlowym wiekiem lub wydatkami."""

    return [
        klient for klient in klienci
        if 0 <= klient["wiek"] <= 120
        and klient["wydatki"] >= 0
    ]


# 2. Normalizacja Min-Max
def normalizuj_pole(klienci, pole):
    """Dodaje znormalizowana wartosc wskazanego pola."""

    if not klienci:
        return []

    minimum = min(klient[pole] for klient in klienci)
    maksimum = max(klient[pole] for klient in klienci)

    zakres = maksimum - minimum

    return [
        {
            **klient,
            f"{pole}_norm": round(
                (klient[pole] - minimum) / zakres, 3
            ) if zakres != 0 else 0.0
        }
        for klient in klienci
    ]


# 3. Segmentacja klientow
def segmentuj(klienci):
    """Przypisuje segment na podstawie dochodu."""

    return [
        {
            **klient,
            "segment": (
                "niski" if klient["dochod"] < 5000
                else "sredni" if klient["dochod"] <= 10000
                else "wysoki"
            )
        }
        for klient in klienci
    ]


# 4. Kompletny pipeline
czyste_dane = usun_outliery(klienci)

dane_norm = normalizuj_pole(czyste_dane, "wiek")
dane_norm = normalizuj_pole(dane_norm, "dochod")

dane_segmentowane = segmentuj(dane_norm)

# 5. Sortowanie wedlug dochodu malejaco
wynik = sorted(
    dane_segmentowane,
    key=lambda klient: klient["dochod"],
    reverse=True
)


# Wyswietlenie wynikow
print("PIPELINE ANALIZY DANYCH KLIENTOW")
print("=" * 85)

print(f"Liczba klientow przed czyszczeniem: {len(klienci)}")
print(f"Liczba klientow po czyszczeniu: {len(czyste_dane)}")
print(f"Liczba usunietych rekordow: {len(klienci) - len(czyste_dane)}")

usuniete_id = [
    klient["id"] for klient in klienci
    if klient not in czyste_dane
]

print(f"ID usunietych klientow: {usuniete_id}")


print("\nDANE PO PRZETWORZENIU")
print("=" * 85)

print(
    f"{'ID':>3} {'Wiek':>6} {'Dochod':>10} "
    f"{'Wydatki':>10} {'Wiek norm':>12} "
    f"{'Dochod norm':>12} {'Segment':>10}"
)

print("-" * 85)

for klient in wynik:
    print(
        f"{klient['id']:>3} "
        f"{klient['wiek']:>6} "
        f"{klient['dochod']:>10} "
        f"{klient['wydatki']:>10} "
        f"{klient['wiek_norm']:>12.3f} "
        f"{klient['dochod_norm']:>12.3f} "
        f"{klient['segment']:>10}"
    )


# Podsumowanie segmentow
print("\nPODSUMOWANIE SEGMENTOW")
print("=" * 85)

segmenty = ["niski", "sredni", "wysoki"]

podsumowanie = {
    segment: sum(
        klient["segment"] == segment
        for klient in wynik
    )
    for segment in segmenty
}

for segment, liczba in podsumowanie.items():
    print(f"{segment:10}: {liczba} klientow")


# Weryfikacja wynikow
print("\nWERYFIKACJA")
print("=" * 85)

print(f"Czy usunieto 2 rekordy: {len(klienci) - len(czyste_dane) == 2}")
print(f"Czy pozostalo 4 klientow: {len(wynik) == 4}")
print(f"Czy usunieto klientow 2 i 3: {usuniete_id == [2, 3]}")

poprawna_normalizacja = all(
    0 <= klient["wiek_norm"] <= 1
    and 0 <= klient["dochod_norm"] <= 1
    for klient in wynik
)

print(f"Czy normalizacja jest poprawna: {poprawna_normalizacja}")

oczekiwane_segmenty = {
    "niski": 1,
    "sredni": 2,
    "wysoki": 1
}

print(f"Czy segmentacja jest poprawna: {podsumowanie == oczekiwane_segmenty}")
