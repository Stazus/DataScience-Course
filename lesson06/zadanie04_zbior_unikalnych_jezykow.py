# Lekcja 06 - Zadanie 4: Zbiór unikalnych języków

# Lista języków programowania
jezyki = ['Python', 'R', 'SQL', 'Python', 'Julia',
          'R', 'Python', 'Scala', 'SQL']

# Utworzenie zbioru unikalnych języków
unikalne = set(jezyki)

print(f"Unikalne języki: {unikalne}")
print(f"Liczba unikalnych języków: {len(unikalne)}")

# Dodanie nowych języków
unikalne.update(['Go', 'Rust'])

# Sprawdzenie obecności języków w zbiorze
print(f"Czy Python jest w zbiorze: {'Python' in unikalne}")
print(f"Czy Fortran jest w zbiorze: {'Fortran' in unikalne}")
print(f"Czy Julia jest w zbiorze: {'Julia' in unikalne}")

# Usunięcie języka Scala
unikalne.discard('Scala')

# Wyświetlenie finalnego zbioru
print(f"Finalny zbiór: {unikalne}")
print(f"Finalna liczba języków: {len(unikalne)}")
