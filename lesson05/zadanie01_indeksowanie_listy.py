# Lekcja 05 - Zadanie 1: Tworzenie i indeksowanie listy

# Temperatury z 7 dni
temperatury = [22.5, 23.0, 21.5, 24.0, 23.5, 22.0, 23.0]

# Indeksowanie listy
pierwszy_dzien = temperatury[0]
ostatni_dzien = temperatury[-1]

# Trzy środkowe dni (indeksy 2, 3, 4)
srodkowe_dni = temperatury[2:5]

# Wyświetlanie wyników
print(f"Temperatura pierwszego dnia: {pierwszy_dzien} °C")
print(f"Temperatura ostatniego dnia: {ostatni_dzien} °C")
print(f"Temperatury trzech środkowych dni: {srodkowe_dni}")
