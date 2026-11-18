# Lekcja 08 - Zadanie 11: Feature engineering z comprehension

# Dane wejsciowe
klienci = [
    {"id": 1, "wiek": 25, "dochod": 4500},
    {"id": 2, "wiek": 45, "dochod": 9200},
    {"id": 3, "wiek": 32, "dochod": 6800},
    {"id": 4, "wiek": 28, "dochod": 5200},
    {"id": 5, "wiek": 55, "dochod": 12000}
]

# Funkcja okreslajaca kategorie wiekowa
def kategoria_wiekowa(wiek):
    if wiek < 30:
        return "młody"
    elif wiek <= 50:
        return "średni"
    else:
        return "starszy"


# Funkcja okreslajaca kategorie dochodu
def kategoria_dochodu(dochod):
    if dochod < 5000:
        return "niski"
    elif dochod <= 10000:
        return "średni"
    else:
        return "wysoki"


# Feature engineering - list comprehension
klienci_rozszerzeni = [
    {
        **klient,
        "kat_wiekowa": kategoria_wiekowa(klient["wiek"]),
        "kat_dochodu": kategoria_dochodu(klient["dochod"])
    }
    for klient in klienci
]

# Wyswietlenie wynikow
print("FEATURE ENGINEERING")
print("=" * 65)

for klient in klienci_rozszerzeni:
    print(klient)

# Wyswietlenie danych w formie tabeli
print("\nDANE KLIENTOW Z NOWYMI CECHAMI")
print("=" * 65)

print(f"{'ID':>3} {'Wiek':>6} {'Dochod':>10} {'Kat. wieku':>15} {'Kat. dochodu':>15}")
print("-" * 65)

for klient in klienci_rozszerzeni:
    print(
        f"{klient['id']:>3} "
        f"{klient['wiek']:>6} "
        f"{klient['dochod']:>10} "
        f"{klient['kat_wiekowa']:>15} "
        f"{klient['kat_dochodu']:>15}"
    )

print("\nLiczba klientow:", len(klienci_rozszerzeni))
print("Liczba nowych cech: 2")
