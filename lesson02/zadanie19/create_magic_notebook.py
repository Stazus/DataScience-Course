import nbformat
from pathlib import Path

notebook = nbformat.v4.new_notebook()

notebook.cells = [
    nbformat.v4.new_markdown_cell(
        "# Test magic commands\n"
        "Notebook do sprawdzania wykrywania poleceń magicznych."
    ),
    nbformat.v4.new_code_cell(
        "%time sum(range(1000))"
    ),
]

output_path = Path("zadanie19/test_magic_notebook.ipynb")

nbformat.write(notebook, output_path)

print(f"Utworzono notebook: {output_path}")
