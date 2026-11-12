# Lekcja 06 - Zadanie 1: Pierwszy słownik studenta

# Utworzenie słownika
student = {
    'imie': 'Kamil',
    'nazwisko': 'Nowak',
    'wiek': 22,
    'kierunek': 'Informatyka'
}

# Dodanie adresu email
student['email'] = 'kamil.nowak@edu.pl'

# Zmiana wieku studenta
student['wiek'] = 23

# Wyświetlenie danych studenta
print(
    f"Student: {student['imie']} {student['nazwisko']} "
    f"({student['wiek']} lata), "
    f"kierunek: {student['kierunek']}, "
    f"email: {student['email']}"
)

# Utworzenie listy kluczy i wartości
klucze = list(student.keys())
wartosci = list(student.values())

# Wyświetlenie list
print(f"Klucze: {klucze}")
print(f"Wartości: {wartosci}")
