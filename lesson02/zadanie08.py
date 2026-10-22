import matplotlib.pyplot as plt


# ==========================================
# ZADANIE 8 - ZAPISYWANIE WYKRESÓW
# ==========================================

# Dane dotyczące zużycia energii
urzadzenia = ["Laptop", "Desktop", "Serwer"]
energia = [30, 150, 400]

# Kolory słupków
kolory = ["royalblue", "orange", "seagreen"]

# Utworzenie wykresu
plt.figure(figsize=(9, 6))

slupki = plt.bar(urzadzenia, energia, color=kolory)

# Tytuł i etykiety osi
plt.title("Porównanie zużycia energii urządzeń")
plt.xlabel("Urządzenie")
plt.ylabel("Zużycie energii (Wh)")

# Wartości nad słupkami
plt.bar_label(slupki, labels=[f"{x} Wh" for x in energia], padding=3)

# Dodatkowe ustawienia
plt.ylim(0, 450)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()

# Zapis wykresu do pliku PNG
plt.savefig("energy_comparison.png", dpi=300)

print("Wykres zapisano jako energy_comparison.png")
