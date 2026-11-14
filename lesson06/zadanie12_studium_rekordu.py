# Lekcja 06 - Zadanie 12: Pelne studium pojedynczego rekordu

# Rekord datasetu Iris
rekord = ('setosa', 5.1, 3.5, 1.4, 0.2)

# Rozpakowanie krotki
gatunek, sl, sw, pl, pw = rekord

# Utworzenie slownika
rekord_slownik = {
    'species': gatunek,
    'sepal_length': sl,
    'sepal_width': sw,
    'petal_length': pl,
    'petal_width': pw
}

# Wyswietlenie danych w formacie tabelarycznym
print("REKORD DATASETU IRIS")
print("-" * 30)

print(f"{'species':<13}: {rekord_slownik['species']}")
print(f"{'sepal_length':<13}: {rekord_slownik['sepal_length']:>5.1f}")
print(f"{'sepal_width':<13}: {rekord_slownik['sepal_width']:>5.1f}")
print(f"{'petal_length':<13}: {rekord_slownik['petal_length']:>5.1f}")
print(f"{'petal_width':<13}: {rekord_slownik['petal_width']:>5.1f}")

# Suma wszystkich cech liczbowych
suma_cech = sum(rekord[1:])

print(f"\nSuma cech liczbowych: {suma_cech:.1f}")
