# Lekcja 05 - Zadanie 7: Zliczanie wystąpień

# Lista predykcji modelu
predykcje = ['spam', 'ham', 'spam', 'spam', 'ham', 'ham', 'spam']

# Zliczanie wystąpień
liczba_spam = predykcje.count('spam')
liczba_ham = predykcje.count('ham')

# Wyświetlanie wyników
print(f"spam: {liczba_spam}, ham: {liczba_ham}")
