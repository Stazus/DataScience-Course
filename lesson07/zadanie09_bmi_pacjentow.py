# Lekcja 07 - Zadanie 9: BMI dla pieciu pacjentow

# Dane pacjentow
wagi = [70, 85, 62, 95, 78]
wzrosty = [1.75, 1.80, 1.65, 1.78, 1.72]

# Obliczanie i klasyfikacja BMI
for i in range(len(wagi)):
    bmi = wagi[i] / wzrosty[i] ** 2

    if bmi < 18.5:
        klasyfikacja = "niedowaga"
    elif bmi < 25.0:
        klasyfikacja = "norma"
    elif bmi < 30.0:
        klasyfikacja = "nadwaga"
    else:
        klasyfikacja = "otyłość"

    print(
        f"Pacjent {i + 1}: waga {wagi[i]} kg, "
        f"wzrost {wzrosty[i]:.2f} m, "
        f"BMI {bmi:.2f} – {klasyfikacja}"
    )
