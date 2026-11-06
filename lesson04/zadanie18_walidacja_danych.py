# Lekcja 04 - Zadanie 18: Walidacja formatu danych wejściowych

# Dane wejściowe
wiek = " 45.7 "
plec = "male"
cisnienie = "120/80"
wzrost = " 175.5cm "

print("=" * 50)
print(f"{'RAPORT WALIDACJI DANYCH':^50}")
print("=" * 50)

# 1. Walidacja wieku
try:
    wiek_liczba = float(wiek.strip())

    if 0 < wiek_liczba <= 120:
        print(f"Wiek:       OK - {wiek_liczba} lat")
    else:
        print("Wiek:       BŁĄD - poza zakresem (0, 120]")
except ValueError:
    print("Wiek:       BŁĄD - niepoprawna liczba")

# 2. Walidacja płci
plec = plec.strip().lower()

if plec in ("male", "female"):
    print(f"Płeć:       OK - {plec}")
else:
    print("Płeć:       BŁĄD - dozwolone male/female")

# 3. Walidacja ciśnienia
try:
    czesci = cisnienie.strip().split("/")

    if len(czesci) != 2:
        raise ValueError("Niepoprawny format")

    skurczowe = int(czesci[0].strip())
    rozkurczowe = int(czesci[1].strip())

    poprawne = (
        70 <= skurczowe <= 250
        and 40 <= rozkurczowe <= 150
        and skurczowe > rozkurczowe
    )

    if poprawne:
        print(f"Ciśnienie:  OK - {skurczowe}/{rozkurczowe} mmHg")
    else:
        print("Ciśnienie:  BŁĄD - niepoprawne wartości")
except ValueError:
    print("Ciśnienie:  BŁĄD - niepoprawny format")

# 4. Walidacja wzrostu
try:
    wzrost_tekst = wzrost.strip().lower()

    if not wzrost_tekst.endswith("cm"):
        raise ValueError("Brak jednostki cm")

    wzrost_liczba = float(wzrost_tekst.removesuffix("cm").strip())

    if 0 < wzrost_liczba <= 300:
        print(f"Wzrost:     OK - {wzrost_liczba} cm")
    else:
        print("Wzrost:     BŁĄD - niepoprawna wartość")
except ValueError:
    print("Wzrost:     BŁĄD - niepoprawny format")

print("=" * 50)
