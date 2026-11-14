# Lekcja 06 - Zadanie 11: Mini-raport z zagniezdzonego slownika

# Dane finansowe
raport = {
    'Q1': {'przychod': 120_000, 'koszt': 80_000},
    'Q2': {'przychod': 145_000, 'koszt': 92_000},
    'Q3': {'przychod': 138_000, 'koszt': 88_000},
    'Q4': {'przychod': 167_000, 'koszt': 101_000}
}

# Przychody poszczegolnych kwartalow
print("PRZYCHODY KWARTALNE")
print(f"Q1: {raport['Q1']['przychod']} zl")
print(f"Q2: {raport['Q2']['przychod']} zl")
print(f"Q3: {raport['Q3']['przychod']} zl")
print(f"Q4: {raport['Q4']['przychod']} zl")

# Obliczenie zyskow kwartalnych
raport['Q1']['zysk'] = raport['Q1']['przychod'] - raport['Q1']['koszt']
raport['Q2']['zysk'] = raport['Q2']['przychod'] - raport['Q2']['koszt']
raport['Q3']['zysk'] = raport['Q3']['przychod'] - raport['Q3']['koszt']
raport['Q4']['zysk'] = raport['Q4']['przychod'] - raport['Q4']['koszt']

# Tabela raportu finansowego
print("\nRAPORT FINANSOWY")
print(f"{'Kwartal':^7} | {'Przychod':>8} | {'Koszt':>8} | {'Zysk':>8}")
print("-" * 40)

print(f"{'Q1':^7} | {raport['Q1']['przychod']:>8} | {raport['Q1']['koszt']:>8} | {raport['Q1']['zysk']:>8}")
print(f"{'Q2':^7} | {raport['Q2']['przychod']:>8} | {raport['Q2']['koszt']:>8} | {raport['Q2']['zysk']:>8}")
print(f"{'Q3':^7} | {raport['Q3']['przychod']:>8} | {raport['Q3']['koszt']:>8} | {raport['Q3']['zysk']:>8}")
print(f"{'Q4':^7} | {raport['Q4']['przychod']:>8} | {raport['Q4']['koszt']:>8} | {raport['Q4']['zysk']:>8}")

# Lista wszystkich zyskow
zyski = [
    raport['Q1']['zysk'],
    raport['Q2']['zysk'],
    raport['Q3']['zysk'],
    raport['Q4']['zysk']
]

# Statystyki zyskow
print("\nPODSUMOWANIE")
print(f"Lista zyskow: {zyski}")
print(f"Suma zyskow: {sum(zyski)} zl")
print(f"Minimalny zysk: {min(zyski)} zl")
print(f"Maksymalny zysk: {max(zyski)} zl")
print(f"Sredni zysk: {sum(zyski) / len(zyski):.2f} zl")
