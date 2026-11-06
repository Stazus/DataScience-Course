# Lekcja 04 - Zadanie 7: Porównanie dwóch modeli

accuracy_a = 0.87
czas_a = 120

accuracy_b = 0.89
czas_b = 450

# Porównanie dokładności
roznica = round(abs(accuracy_a - accuracy_b), 4)
znaczaca_roznica = roznica > 0.02

# Porównanie czasu trenowania
a_szybszy = czas_a < czas_b
b_szybszy = czas_b < czas_a

print(f"Model A: accuracy = {accuracy_a:.2%}, czas = {czas_a} s")
print(f"Model B: accuracy = {accuracy_b:.2%}, czas = {czas_b} s")

print(f"\nRóżnica accuracy: {roznica:.2%}")
print(f"Różnica znacząca: {znaczaca_roznica}")

# Wybór najlepszego kompromisu
if znaczaca_roznica and accuracy_a > accuracy_b:
    rekomendacja = "Model A"
elif znaczaca_roznica and accuracy_b > accuracy_a:
    rekomendacja = "Model B"
elif a_szybszy:
    rekomendacja = "Model A"
elif b_szybszy:
    rekomendacja = "Model B"
else:
    rekomendacja = "Oba modele są porównywalne"

print(f"\nRekomendacja: {rekomendacja}")
