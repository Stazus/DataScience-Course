# Lekcja 04 - Zadanie 8: Obliczanie learning rate

lr_initial = 0.1
decay = 0.95
epoch = 10

# Obliczenie learning rate po 10 epokach
lr_new = lr_initial * (decay ** epoch)

# Wyświetlenie wyniku w notacji naukowej
print(f"Learning rate po {epoch} epokach: {lr_new:.2e}")
