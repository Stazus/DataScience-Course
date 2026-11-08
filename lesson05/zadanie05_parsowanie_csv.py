# Lekcja 05 - Zadanie 5: Parsowanie linii CSV

# Dane wejściowe
linia = "Alice,28,Data Scientist,75000"

# Podział tekstu na pola
pola = linia.split(",")

# Pobieranie i konwersja danych
imie = pola[0]
wiek = int(pola[1])
zawod = pola[2]
pensja = int(pola[3])

# Wyświetlanie wyników
print(f"Pola CSV: {pola}")
print(f"Imię: {imie}")
print(f"Wiek: {wiek}")
print(f"Zawód: {zawod}")
print(f"Pensja: {pensja}")

# Wynik wymagany w zadaniu
print(f"{imie} ma {wiek} lat, pracuje jako {zawod} i zarabia ${pensja}")
