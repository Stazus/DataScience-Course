# Lekcja 11 - Zadanie 1: Tworzenie DataFrame z danych

import pandas as pd


# Slownik zawierajacy dane 10 produktow
dane = {
    "Nazwa": [
        "Laptop",
        "Monitor",
        "Klawiatura",
        "Mysz",
        "Sluchawki",
        "Smartfon",
        "Tablet",
        "Drukarka",
        "Pendrive",
        "Dysk SSD"
    ],
    "Cena": [
        3500.00, 1200.00, 250.00, 80.00, 350.00,
        2200.00, 1500.00, 650.00, 60.00, 400.00
    ],
    "Ilosc": [
        12, 20, 35, 50, 25,
        15, 18, 10, 80, 30
    ],
    "Kategoria": [
        "Komputery",
        "Monitory",
        "Akcesoria",
        "Akcesoria",
        "Audio",
        "Mobilne",
        "Mobilne",
        "Urzadzenia biurowe",
        "Pamiec",
        "Pamiec"
    ]
}

# Tworzenie DataFrame ze slownika
df = pd.DataFrame(dane)

print("TWORZENIE DATAFRAME Z DANYCH")
print("=" * 75)

# Pierwsze 5 wierszy
print("\nPIERWSZE 5 WIERSZY")
print("=" * 75)
print(df.head().to_string(index=False))

# Obliczenie wartosci towaru
df["WartośćCałkowita"] = df["Cena"] * df["Ilosc"]

# Wyswietlenie kompletnego DataFrame
print("\nPELNY DATAFRAME")
print("=" * 75)
print(df.to_string(index=False))

# Podstawowe informacje
print("\nINFORMACJE O DATAFRAME")
print("=" * 75)
print(f"Shape: {df.shape}")
print(f"Liczba produktow: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print(f"Nazwy kolumn: {df.columns.tolist()}")

print("\nTypy danych:")
print(df.dtypes)

# Podsumowanie magazynu
print("\nPODSUMOWANIE MAGAZYNU")
print("=" * 75)
print(f"Liczba sztuk: {df['Ilosc'].sum()}")
print(f"Srednia cena: {df['Cena'].mean():.2f} PLN")
print(f"Wartosc magazynu: {df['WartośćCałkowita'].sum():.2f} PLN")

# Liczba produktow wedlug kategorii
print("\nPRODUKTY WEDLUG KATEGORII")
print("=" * 75)
print(df["Kategoria"].value_counts().to_string())

# Weryfikacja
print("\nWERYFIKACJA")
print("=" * 75)
print(f"Czy DataFrame zawiera 10 produktow: {len(df) == 10}")
print(f"Czy DataFrame ma 5 kolumn: {df.shape[1] == 5}")
print(f"Czy dodano nowa kolumne: {'WartośćCałkowita' in df.columns}")
print(f"Czy wartosci sa poprawne: {(df['WartośćCałkowita'] == df['Cena'] * df['Ilosc']).all()}")
print(f"Czy ceny sa dodatnie: {(df['Cena'] > 0).all()}")
print(f"Czy ilosci sa nieujemne: {(df['Ilosc'] >= 0).all()}")
print(f"Czy brak pustych wartosci: {not df.isna().any().any()}")
