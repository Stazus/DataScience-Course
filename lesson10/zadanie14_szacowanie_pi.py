# Lekcja 10 - Zadanie 14: Oszacowanie pi metoda siatki

import numpy as np


# Rozmiar siatki
n = 1000

# Tworzenie wspolrzednych od -1 do 1
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)

# Tworzenie dwuwymiarowej siatki punktow
X, Y = np.meshgrid(x, y)

# Wektorowe sprawdzenie, czy punkty naleza do kola
maska_kola = X**2 + Y**2 <= 1

# Liczenie punktow
liczba_wszystkich = maska_kola.size
liczba_w_kole = np.count_nonzero(maska_kola)
liczba_poza_kolem = liczba_wszystkich - liczba_w_kole

# Oszacowanie liczby pi
pi_oszacowane = 4 * liczba_w_kole / liczba_wszystkich

# Obliczenie bledow
blad_bezwzgledny = abs(pi_oszacowane - np.pi)
blad_wzgledny = blad_bezwzgledny / np.pi * 100

# Mapa pierwszych 20x20 punktow
mapa = np.where(maska_kola[:20, :20], "●", "·")

# Dodatkowa mapa pogladowa calego kola
indeksy = np.linspace(0, n - 1, 20, dtype=int)
maska_pogladowa = maska_kola[np.ix_(indeksy, indeksy)]
mapa_pogladowa = np.where(maska_pogladowa, "●", "·")


print("OSZACOWANIE PI METODA SIATKI")
print("=" * 75)

print("\nPARAMETRY SIATKI")
print("=" * 75)
print(f"Rozmiar siatki: {n} x {n}")
print(f"Shape X: {X.shape}")
print(f"Shape Y: {Y.shape}")
print(f"Liczba wszystkich punktow: {liczba_wszystkich:,}")

print("\nANALIZA PUNKTOW")
print("=" * 75)
print(f"Punkty w kole: {liczba_w_kole:,}")
print(f"Punkty poza kolem: {liczba_poza_kolem:,}")
print(f"Procent punktow w kole: {liczba_w_kole / liczba_wszystkich * 100:.4f}%")

print("\nOSZACOWANIE LICZBY PI")
print("=" * 75)
print(f"Pi oszacowane: {pi_oszacowane:.10f}")
print(f"Pi rzeczywiste: {np.pi:.10f}")
print(f"Blad bezwzgledny: {blad_bezwzgledny:.10f}")
print(f"Blad wzgledny: {blad_wzgledny:.6f}%")

print("\nMAPA PIERWSZYCH 20x20 PUNKTOW")
print("=" * 75)
print("Legenda: ● - w kole, · - poza kolem")

# Petla sluzy wylacznie do wyswietlania
for wiersz in mapa:
    print(" ".join(wiersz))

print("\nDODATKOWA MAPA POGLADOWA CALEGO KOLA")
print("=" * 75)

for wiersz in mapa_pogladowa:
    print(" ".join(wiersz))

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy X ma ksztalt (1000, 1000): {X.shape == (1000, 1000)}")
print(f"Czy Y ma ksztalt (1000, 1000): {Y.shape == (1000, 1000)}")
print(f"Czy siatka ma milion punktow: {liczba_wszystkich == 1000000}")
print(f"Czy maska ma typ bool: {maska_kola.dtype == np.bool_}")
print(f"Czy suma punktow jest poprawna: {liczba_w_kole + liczba_poza_kolem == liczba_wszystkich}")
print(f"Czy maska jest symetryczna: {np.array_equal(maska_kola, maska_kola.T)}")
print(f"Czy oszacowanie pi jest poprawne: {np.isclose(pi_oszacowane, np.pi, atol=0.01, rtol=0)}")
print(f"Czy blad wzgledny jest mniejszy niz 1%: {blad_wzgledny < 1}")
print(f"Czy pierwsza mapa ma ksztalt (20, 20): {mapa.shape == (20, 20)}")
print(f"Czy mapa pogladowa ma ksztalt (20, 20): {mapa_pogladowa.shape == (20, 20)}")
