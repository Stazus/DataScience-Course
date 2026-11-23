# Lekcja 10 - Zadanie 17: Operacje na obrazie (NumPy only)

import numpy as np


# Generowanie obrazu w skali szarosci
np.random.seed(6)

image = np.random.randint(
    0, 256, size=(100, 100), dtype=np.uint8
)

# Kopia obrazu oryginalnego
image_original = image.copy()

# Progowanie - Boolean indexing
threshold = image.copy()

threshold[image < 128] = 0
threshold[image >= 128] = 255

# Negatyw obrazu
negative = 255 - image

# Padding - czarna ramka o szerokosci 10 pikseli
padded = np.pad(
    image,
    pad_width=10,
    mode="constant",
    constant_values=0
)


def wyswietl_obraz(nazwa, obraz):
    print(f"\n{nazwa}")
    print("=" * 75)

    print(f"Shape: {obraz.shape}")
    print(f"Typ danych: {obraz.dtype}")
    print(f"Liczba pikseli: {obraz.size}")
    print(f"Minimum: {np.min(obraz)}")
    print(f"Maksimum: {np.max(obraz)}")

    print("\nWartosci rogowe (po 5 pikseli):")
    print(f"Lewy gorny rog:  {obraz[0, :5]}")
    print(f"Prawy gorny rog: {obraz[0, -5:]}")
    print(f"Lewy dolny rog:  {obraz[-1, :5]}")
    print(f"Prawy dolny rog: {obraz[-1, -5:]}")


print("OPERACJE NA OBRAZIE - NUMPY")
print("=" * 75)

wyswietl_obraz("OBRAZ ORYGINALNY", image)

wyswietl_obraz("OBRAZ PO PROGOWANIU", threshold)

wyswietl_obraz("NEGATYW OBRAZU", negative)

wyswietl_obraz("OBRAZ Z RAMKA - PADDING", padded)


# Statystyki progowania
czarne_piksele = np.count_nonzero(threshold == 0)
biale_piksele = np.count_nonzero(threshold == 255)

print("\nSTATYSTYKI PROGOWANIA")
print("=" * 75)

print(f"Czarne piksele: {czarne_piksele}")
print(f"Biale piksele: {biale_piksele}")

print(f"Procent czarnych: {czarne_piksele / image.size * 100:.2f}%")
print(f"Procent bialych: {biale_piksele / image.size * 100:.2f}%")


# Weryfikacja czarnej ramki
ramka_poprawna = (
    np.all(padded[:10, :] == 0)
    and np.all(padded[-10:, :] == 0)
    and np.all(padded[:, :10] == 0)
    and np.all(padded[:, -10:] == 0)
)

print("\nSTATYSTYKI PADDINGU")
print("=" * 75)

print(f"Piksele przed paddingiem: {image.size}")
print(f"Piksele po paddingu: {padded.size}")
print(f"Liczba dodanych pikseli: {padded.size - image.size}")


print("\nWERYFIKACJA")
print("=" * 75)

print(f"Czy obraz ma ksztalt (100, 100): "
      f"{image.shape == (100, 100)}")

print(f"Czy obraz ma typ uint8: "
      f"{image.dtype == np.uint8}")

print(f"Czy progowanie zachowalo ksztalt: "
      f"{threshold.shape == image.shape}")

print(f"Czy progowanie zawiera tylko 0 i 255: "
      f"{np.all(np.isin(threshold, [0, 255]))}")

print(f"Czy piksele ponizej 128 zmieniono na 0: "
      f"{np.all(threshold[image < 128] == 0)}")

print(f"Czy piksele od 128 zmieniono na 255: "
      f"{np.all(threshold[image >= 128] == 255)}")

print(f"Czy negatyw jest poprawny: "
      f"{np.all(image.astype(int) + negative.astype(int) == 255)}")

print(f"Czy padding ma ksztalt (120, 120): "
      f"{padded.shape == (120, 120)}")

print(f"Czy ramka zawiera same zera: "
      f"{ramka_poprawna}")

print(f"Czy padding zachowal obraz wewnetrzny: "
      f"{np.array_equal(padded[10:-10, 10:-10], image)}")

print(f"Czy dodano 4400 pikseli: "
      f"{padded.size - image.size == 4400}")

print(f"Czy obraz oryginalny pozostal niezmieniony: "
      f"{np.array_equal(image, image_original)}")
