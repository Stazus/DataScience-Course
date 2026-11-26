# Lekcja 13 - Zadanie 1: Podstawowy SELECT

import sqlite3
import pandas as pd


def section(title):
    """Wyświetla nagłówek sekcji."""
    print(f"\n{title}")
    print("=" * 75)


# 1. Utworzenie bazy danych SQLite w pamięci
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()


# 2. Utworzenie tabeli products
cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
""")


# 3. Przygotowanie 10 przykładowych produktów
products = [
    (1, "Laptop", "Elektronika", 3500.00, 10),
    (2, "Mysz", "Akcesoria", 50.00, 150),
    (3, "Klawiatura", "Akcesoria", 200.00, 80),
    (4, "Monitor", "Elektronika", 1200.00, 25),
    (5, "Słuchawki", "Akcesoria", 150.00, 60),
    (6, "Smartfon", "Elektronika", 2500.00, 30),
    (7, "Tablet", "Elektronika", 1800.00, 20),
    (8, "Pendrive", "Pamięć", 45.00, 100),
    (9, "Dysk SSD", "Pamięć", 350.00, 40),
    (10, "Drukarka", "Elektronika", 650.00, 15),
]


# 4. Wstawienie danych do tabeli
cursor.executemany("""
    INSERT INTO products (
        product_id, name, category, price, stock
    )
    VALUES (?, ?, ?, ?, ?)
""", products)

conn.commit()


# 5. SELECT - wszystkie produkty
section("1. WSZYSTKIE PRODUKTY")

query_all = """
SELECT *
FROM products
"""

df_all = pd.read_sql_query(query_all, conn)

print(df_all.to_string(index=False))


# 6. SELECT - wybrane kolumny
section("2. NAZWA I CENA PRODUKTÓW")

query_selected = """
SELECT name, price
FROM products
"""

df_selected = pd.read_sql_query(query_selected, conn)

print(df_selected.to_string(index=False))


# 7. Automatyczna weryfikacja wyników
section("3. AUTOMATYCZNE TESTY")

assert len(df_all) == 10
print("[OK] Tabela zawiera 10 produktów")

assert df_all.shape == (10, 5)
print("[OK] Pierwsze zapytanie zwraca 10 wierszy i 5 kolumn")

assert df_all["product_id"].is_unique
print("[OK] Identyfikatory produktów są unikalne")

assert df_selected.shape == (10, 2)
print("[OK] Drugie zapytanie zwraca 10 wierszy i 2 kolumny")

assert list(df_selected.columns) == ["name", "price"]
print("[OK] Wybrano właściwe kolumny")

assert df_selected.equals(df_all[["name", "price"]])
print("[OK] Dane z obu zapytań są zgodne")

assert not df_all.isna().any().any()
print("[OK] Brak brakujących wartości")


# 8. Zamknięcie połączenia
conn.close()


section("PODSUMOWANIE")

print("Liczba produktów:", len(df_all))
print("Liczba wykonanych zapytań SELECT: 2")
print("Wszystkie 7 testów zakończone sukcesem.")
print("Zadanie 1 wykonane poprawnie.")
