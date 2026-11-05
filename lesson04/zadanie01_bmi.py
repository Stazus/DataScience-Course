# Lekcja 04 - Zadanie 1: Kalkulator BMI

waga = 70
wzrost = 1.75

bmi = waga / (wzrost ** 2)

if bmi < 18.5:
    interpretacja = "Niedowaga"
elif bmi < 25:
    interpretacja = "Norma"
else:
    interpretacja = "Nadwaga"

print(f"BMI: {bmi:.2f}")
print(f"Interpretacja: {interpretacja}")
