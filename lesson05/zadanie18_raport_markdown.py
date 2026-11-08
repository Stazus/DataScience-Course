# Lekcja 05 - Zadanie 18: Generowanie raportu Markdown

# Dane trzech eksperymentów
e1 = ["Exp_01", 0.85, 1.23]
e2 = ["Exp_02", 0.89, 4.56]
e3 = ["Exp_03", 0.87, 7.89]

# Tworzenie listy wierszy raportu
wiersze = [
    "# Raport",
    "",
    "| Experiment | Accuracy | Time |",
    "|------------|----------|------|",
    f"| {e1[0]} | {e1[1]:.2%} | {e1[2]:.2f}s |",
    f"| {e2[0]} | {e2[1]:.2%} | {e2[2]:.2f}s |",
    f"| {e3[0]} | {e3[1]:.2%} | {e3[2]:.2f}s |"
]

# Łączenie wierszy w jeden tekst
raport = "\n".join(wiersze)

# Wyświetlenie raportu Markdown
print(raport)
