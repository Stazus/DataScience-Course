import nbformat

notebook = nbformat.v4.new_notebook()

notebook.cells = [
    nbformat.v4.new_markdown_cell(
        "# Test monitorowania zasobów"
    ),
    nbformat.v4.new_code_cell(
        """
import time

print("Rozpoczynam test...")

for i in range(10):
    print(f"Krok {i + 1}/10")
    time.sleep(1)

print("Test zakończony.")
"""
    )
]

nbformat.write(notebook, "test_zadanie14.ipynb")

print("Utworzono notebook test_zadanie14.ipynb")
