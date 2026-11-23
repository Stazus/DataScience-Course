# Lekcja 10 - Zadanie 19: Przygotowanie cech do regresji wielomianowej

import numpy as np


# Generowanie danych
np.random.seed(7)

x = np.linspace(0, 10, 100)

y = 2 * x**2 - 3 * x + 5 + np.random.randn(100) * 10

# Kopie danych oryginalnych
x_original = x.copy()
y_original = y.copy()

# Przygotowanie poszczegolnych cech
jedynki = np.ones_like(x)
x_kwadrat = x**2

# Macierz cech dla regresji wielomianowej stopnia 2
X = np.column_stack((jedynki, x, x_kwadrat))

# Statystyki kolumny x^2
srednia_x2 = np.mean(X[:, 2])
odchylenie_x2 = np.std(X[:, 2])

# Ustawienia wyswietlania
np.set_printoptions(precision=4, suppress=True)


print("PRZYGOTOWANIE CECH DO REGRESJI WIELOMIANOWEJ")
print("=" * 75)

print("\nDANE WEJSCIOWE")
print("=" * 75)
print("Rownanie: y = 2*x^2 - 3*x + 5 + szum")
print(f"Shape x: {x.shape}")
print(f"Shape y: {y.shape}")
print(f"Liczba probek: {len(x)}")
print(f"Zakres x: [{x.min()}, {x.max()}]")

print("\nMACIERZ CECH X")
print("=" * 75)
print(f"Shape X: {X.shape}")
print(f"Liczba probek: {X.shape[0]}")
print(f"Liczba kolumn: {X.shape[1]}")
print("Kolumny: [1, x, x^2]")

print("\nPIERWSZE 5 WIERSZY MACIERZY X")
print("=" * 75)
print(X[:5])

print("\nPIERWSZE 5 WARTOSCI Y")
print("=" * 75)
print(y[:5])

print("\nSTATYSTYKI KOLUMNY X^2")
print("=" * 75)
print(f"Srednia: {srednia_x2:.4f}")
print(f"Odchylenie standardowe: {odchylenie_x2:.4f}")
print(f"Minimum: {np.min(X[:, 2]):.4f}")
print(f"Maksimum: {np.max(X[:, 2]):.4f}")

print("\nSTATYSTYKI WSZYSTKICH CECH")
print("=" * 75)
print(f"Srednie: {np.mean(X, axis=0)}")
print(f"Odchylenia standardowe: {np.std(X, axis=0)}")
print(f"Minima: {np.min(X, axis=0)}")
print(f"Maksima: {np.max(X, axis=0)}")

print("\nOSTATNIE 5 WIERSZY MACIERZY X")
print("=" * 75)
print(X[-5:])

print("\nPODSUMOWANIE")
print("=" * 75)
print("Stopien wielomianu: 2")
print("Macierz cech: [1, x, x^2]")
print("Model: y = beta_0 + beta_1*x + beta_2*x^2")
print("Macierz X jest przygotowana do regresji.")

print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy x ma 100 elementow: {x.shape == (100,)}")
print(f"Czy y ma 100 elementow: {y.shape == (100,)}")
print(f"Czy X ma ksztalt (100, 3): {X.shape == (100, 3)}")
print(f"Czy pierwsza kolumna zawiera jedynki: {np.all(X[:, 0] == 1)}")
print(f"Czy druga kolumna zawiera x: {np.array_equal(X[:, 1], x)}")
print(f"Czy trzecia kolumna zawiera x^2: {np.allclose(X[:, 2], x**2)}")
print(f"Czy srednia x^2 jest poprawna: {np.isclose(srednia_x2, np.mean(x**2))}")
print(f"Czy std x^2 jest poprawne: {np.isclose(odchylenie_x2, np.std(x**2))}")
print(f"Czy wszystkie wartosci X sa skonczone: {np.all(np.isfinite(X))}")
print(f"Czy wszystkie wartosci y sa skonczone: {np.all(np.isfinite(y))}")
print(f"Czy dane x pozostaly niezmienione: {np.array_equal(x, x_original)}")
print(f"Czy dane y pozostaly niezmienione: {np.array_equal(y, y_original)}")
