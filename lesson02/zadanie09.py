import pandas as pd

# ==========================================
# ZADANIE 9 - PORÓWNANIE COLAB VS LOCAL
# ==========================================

# Dane do porównania środowisk
dane = {
    "Feature": [
        "Koszt",
        "Dostęp do GPU",
        "Praca offline",
        "Limity czasowe",
        "Kontrola środowiska"
    ],
    "Google Colab": [
        "Darmowy plan, płatne opcje",
        "GPU w chmurze, zależnie od dostępności",
        "Zasadniczo wymaga internetu",
        "Ograniczenia czasu sesji",
        "Ograniczona przez platformę"
    ],
    "Jupyter Local": [
        "Darmowy, koszt własnego sprzętu",
        "Zależy od sprzętu i konfiguracji",
        "Tak",
        "Brak limitu narzuconego przez usługę",
        "Pełna kontrola lokalna"
    ]
}

# Utworzenie DataFrame
df = pd.DataFrame(dane)

# Wyświetlenie tabeli
print("PORÓWNANIE GOOGLE COLAB VS JUPYTER LOCAL")
print(df.to_string(index=False))

# Eksport do CSV
df.to_csv("colab_vs_local.csv", index=False, encoding="utf-8-sig")

print("\nTabela została zapisana do pliku colab_vs_local.csv")

# ==========================================
# BONUS - WIZUALIZACJA PORÓWNANIA
# ==========================================

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(15, 5))
ax.axis("off")

tabela = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc="left",
    colLoc="center",
    loc="center",
    colWidths=[0.22, 0.39, 0.39]
)

tabela.auto_set_font_size(False)
tabela.set_fontsize(9)
tabela.scale(1, 2.5)

# Wyróżnienie nagłówków
for (wiersz, kolumna), komorka in tabela.get_celld().items():
    if wiersz == 0:
        komorka.set_facecolor("steelblue")
        komorka.set_text_props(color="white", weight="bold")
    elif wiersz % 2 == 0:
        komorka.set_facecolor("#eef3f8")

plt.title(
    "Google Colab vs Jupyter Local - porównanie środowisk",
    fontsize=14,
    fontweight="bold",
    pad=20
)

plt.savefig(
    "colab_vs_local.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Wizualizacja została zapisana do pliku colab_vs_local.png")
