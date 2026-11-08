# Lekcja 05 - Zadanie 14: Ekstrakcja metadanych z nazwy pliku

# Dane wejściowe
sciezka = "/data/processed/2024/experiment_42_v3.csv"

# Podział ścieżki na elementy
elementy = sciezka.split("/")

# Wyodrębnienie nazwy pliku
nazwa_pliku = elementy[-1]

# Wyodrębnienie katalogu
katalog = sciezka.rsplit("/", 1)[0]

# Oddzielenie nazwy od rozszerzenia
nazwa_bez_rozszerzenia = nazwa_pliku.rsplit(".", 1)[0]
rozszerzenie = "." + nazwa_pliku.rsplit(".", 1)[1]

# Wyodrębnienie roku z katalogu
rok = elementy[-2]

# Wyświetlanie raportu z wyrównaniem
print("METADANE PLIKU")
print("-" * 55)
print(f"{'Nazwa pliku:':25}{nazwa_pliku}")
print(f"{'Katalog:':25}{katalog}")
print(f"{'Nazwa bez rozszerzenia:':25}{nazwa_bez_rozszerzenia}")
print(f"{'Rozszerzenie:':25}{rozszerzenie}")
print(f"{'Rok:':25}{rok}")
