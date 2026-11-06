# Lekcja 04 - Zadanie 19: Kalkulator accuracy z threshold-em

# Dane wejściowe
prawdopodobienstwa = [0.23, 0.67, 0.89, 0.34, 0.91, 0.12, 0.78, 0.45]
prawdziwe_klasy = [0, 1, 1, 0, 1, 0, 1, 0]

progi = [0.3, 0.5, 0.7]

wyniki = {}

print("=" * 55)
print(f"{'PORÓWNANIE PROGÓW KLASYFIKACJI':^55}")
print("=" * 55)

for prog in progi:
    # Zamiana prawdopodobieństw na klasy 0 lub 1
    predykcje = []

    for prawdopodobienstwo in prawdopodobienstwa:
        if prawdopodobienstwo >= prog:
            predykcje.append(1)
        else:
            predykcje.append(0)

    # Liczenie poprawnych predykcji
    poprawne = 0

    for przewidywana, prawdziwa in zip(predykcje, prawdziwe_klasy):
        if przewidywana == prawdziwa:
            poprawne += 1

    # Obliczenie accuracy
    accuracy = poprawne / len(prawdziwe_klasy)
    wyniki[prog] = accuracy

    print(f"Threshold: {prog:.1f}")
    print(f"Predykcje: {predykcje}")
    print(f"Poprawne:  {poprawne}/{len(prawdziwe_klasy)}")
    print(f"Accuracy:  {accuracy:.2%}")
    print("-" * 55)

# Wybór najlepszego wyniku
najlepsza_accuracy = max(wyniki.values())

najlepsze_progi = [
    prog for prog, accuracy in wyniki.items()
    if accuracy == najlepsza_accuracy
]

print(f"Najlepsza accuracy: {najlepsza_accuracy:.2%}")
print(f"Optymalne progi: {najlepsze_progi}")
print("=" * 55)
