# Lekcja 07 - Zadanie 7: Tabliczka mnozenia

liczba = 7

# Tabliczka mnozenia od 1 do 10
for i in range(1, 11):
    wynik = liczba * i
    lewa_kolumna = f"{liczba} × {i}"
    print(f"{lewa_kolumna:<8}= {wynik}")
