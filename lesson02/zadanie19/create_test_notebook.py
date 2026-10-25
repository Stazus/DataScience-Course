import nbformat
from pathlib import Path

notebook = nbformat.v4.new_notebook()

notebook.cells = [
    nbformat.v4.new_markdown_cell(
        "# Analiza danych\n"
        "Notebook testowy do sprawdzania jakości kodu."
    ),

    nbformat.v4.new_markdown_cell(
        "## Przygotowanie danych\n"
        "Ustawiamy ziarno losowości dla powtarzalności wyników."
    ),

    nbformat.v4.new_code_cell(
        "import random\n"
        "random.seed(42)\n"
        "numbers = [1, 2, 3, 4, 5]"
    ),

    nbformat.v4.new_markdown_cell(
        "## Analiza\n"
        "Obliczamy średnią z przygotowanych danych."
    ),

    nbformat.v4.new_code_cell(
        "# Obliczenie średniej\n"
        "average = sum(numbers) / len(numbers)\n"
        "print(average)"
    ),
]

output_path = Path("zadanie19/test_good_notebook.ipynb")

nbformat.write(notebook, output_path)

print(f"Utworzono notebook: {output_path}")
