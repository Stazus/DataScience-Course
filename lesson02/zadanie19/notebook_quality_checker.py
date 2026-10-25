from pathlib import Path
import nbformat
import ast
import sys
import json
from IPython.core.interactiveshell import InteractiveShell


def calculate_nesting_depth(source):
    try:
        transformed_source = InteractiveShell.instance().transform_cell(source)
        tree = ast.parse(transformed_source)
    except (SyntaxError, ValueError):
        return None

    nesting_types = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
        ast.With,
        ast.AsyncWith,
    )

    def visit(node, depth=0):
        if isinstance(node, nesting_types):
            depth += 1

        maximum = depth

        for child in ast.iter_child_nodes(node):
            maximum = max(maximum, visit(child, depth))

        return maximum

    return visit(tree)

def analyze_notebook(notebook_path):
    notebook_path = Path(notebook_path)

    if not notebook_path.is_file():
        print(f"BŁĄD: Nie znaleziono pliku notebooka: {notebook_path}")
        return

    try:
        with notebook_path.open("r", encoding="utf-8") as file:
            raw_notebook = json.load(file)
    except (json.JSONDecodeError, UnicodeError, OSError):
        raw_notebook = None

    if isinstance(raw_notebook, dict):
        raw_cells = raw_notebook.get("cells", [])

        if isinstance(raw_cells, list):
            missing_ids = [
                index
                for index, cell in enumerate(raw_cells, start=1)
                if isinstance(cell, dict) and not cell.get("id")
            ]

            if missing_ids:
                print("BŁĄD: Wykryto komórki bez identyfikatora ID.")
                print(f"Numery komórek: {missing_ids}")
                return

    try:
        notebook = nbformat.read(notebook_path, as_version=4)
    except (json.JSONDecodeError, nbformat.reader.NotJSONError):
        print(f"BŁĄD: Nieprawidłowy format JSON: {notebook_path}")
        return
    except (OSError, UnicodeError) as error:
        print(f"BŁĄD: Nie można odczytać notebooka: {error}")
        return

    try:
        nbformat.validate(notebook)
    except nbformat.ValidationError as error:
        print(f"BŁĄD: Nieprawidłowa struktura notebooka: {notebook_path}")
        print(f"Szczegóły: {error.message}")
        return

    missing_ids = []

    for index, cell in enumerate(notebook.cells, start=1):
        if not cell.get("id"):
            missing_ids.append(index)

    if missing_ids:
        print("BŁĄD: Wykryto komórki bez identyfikatora ID.")
        print(f"Numery komórek: {missing_ids}")
        return

    code_cells = [
        cell for cell in notebook.cells
        if cell.cell_type == "code"
    ]

    markdown_cells = [
        cell for cell in notebook.cells
        if cell.cell_type == "markdown"
    ]

    print(f"Notebook: {notebook_path.name}")
    print(f"Wszystkie komórki: {len(notebook.cells)}")
    print(f"Komórki kodu: {len(code_cells)}")
    print(f"Komórki Markdown: {len(markdown_cells)}")

    total_cells = len(notebook.cells)

    if total_cells > 0:
        markdown_percentage = len(markdown_cells) / total_cells * 100
    else:
        markdown_percentage = 0

    print(f"Udział Markdown: {markdown_percentage:.1f}%")

    if markdown_percentage >= 20:
        print("Markdown: OK (minimum 20%)")
    else:
        print("Markdown: DO POPRAWY (poniżej 20%)")

    comment_lines = 0
    code_lines = 0

    for cell in code_cells:
        for line in cell.source.splitlines():
            stripped_line = line.strip()

            if not stripped_line:
                continue

            code_lines += 1

            if stripped_line.startswith("#"):
                comment_lines += 1

    if code_lines > 0:
        comment_percentage = comment_lines / code_lines * 100
    else:
        comment_percentage = 0

    print(f"Liczba linii kodu i komentarzy: {code_lines}")
    print(f"Liczba komentarzy: {comment_lines}")
    print(f"Udział komentarzy: {comment_percentage:.1f}%")

    documentation_ok = (
        markdown_percentage >= 20
        or comment_percentage >= 20
    )

    if documentation_ok:
        print("Dokumentacja notebooka: OK")
    else:
        print("Dokumentacja notebooka: DO POPRAWY")
        print(
            "Rekomendacja: dodaj komórki Markdown "
            "lub komentarze wyjaśniające kod."
        )

    magic_commands = []

    for cell in code_cells:
        for line in cell.source.splitlines():
            stripped_line = line.strip()

            if stripped_line.startswith("%"):
                magic_commands.append(stripped_line)

    print(f"Liczba magic commands: {len(magic_commands)}")

    if magic_commands:
        print("Wykryte magic commands:")

        for command in magic_commands:
            print(f"  - {command}")
    else:
        print("Magic commands: nie wykryto")

    seed_patterns = [
        "random.seed(",
        "np.random.seed(",
        "numpy.random.seed(",
        "torch.manual_seed(",
        "tf.random.set_seed(",
    ]

    detected_seeds = []

    for cell in code_cells:
        for line in cell.source.splitlines():
            stripped_line = line.strip()

            if any(pattern in stripped_line for pattern in seed_patterns):
                detected_seeds.append(stripped_line)

    if detected_seeds:
        print("Random seed: WYKRYTO")

        for seed in detected_seeds:
            print(f"  - {seed}")
    else:
        print("Random seed: NIE WYKRYTO")
        print(
            "Rekomendacja: jeśli notebook wykorzystuje losowość, "
            "ustaw ziarno losowości dla powtarzalności wyników."
        )

    savefig_patterns = [
        "plt.savefig(",
        "fig.savefig(",
        "pyplot.savefig(",
    ]

    detected_saves = []

    for cell in code_cells:
        for line in cell.source.splitlines():
            stripped_line = line.strip()

            if any(
                pattern in stripped_line
                for pattern in savefig_patterns
            ):
                detected_saves.append(stripped_line)

    if detected_saves:
        print("Zapisywanie wykresów: WYKRYTO")

        for command in detected_saves:
            print(f"  - {command}")
    else:
        print("Zapisywanie wykresów: NIE WYKRYTO")
        print(
            "Rekomendacja: jeśli notebook tworzy wykresy, "
            "rozważ zapisywanie ich do plików."
        )

    print("\nKontrola best practices:")

    if notebook.cells:
        first_cell = notebook.cells[0]

        if first_cell.cell_type == "markdown":
            print("Komórka Markdown na początku: OK")
        else:
            print("Komórka Markdown na początku: DO POPRAWY")
            print(
                "Rekomendacja: rozpocznij notebook "
                "od komórki Markdown z tytułem i opisem."
            )
    else:
        print("Notebook jest pusty: DO POPRAWY")

    empty_cells = []

    for index, cell in enumerate(notebook.cells, start=1):
        if not cell.source.strip():
            empty_cells.append(index)

    if empty_cells:
        print(f"Puste komórki: WYKRYTO ({len(empty_cells)})")
        print(f"Numery pustych komórek: {empty_cells}")
        print(
            "Rekomendacja: usuń puste komórki "
            "lub uzupełnij ich zawartość."
        )
    else:
        print("Puste komórki: NIE WYKRYTO")

    print("\nAnaliza złożoności kodu:")

    long_cells = []

    for index, cell in enumerate(notebook.cells, start=1):
        if cell.cell_type != "code":
            continue

        lines = [
            line for line in cell.source.splitlines()
            if line.strip()
        ]

        line_count = len(lines)

        print(f"Komórka {index}: {line_count} niepustych linii")

        if line_count > 30:
            long_cells.append(index)

    if long_cells:
        print(f"Zbyt długie komórki: {long_cells}")
        print(
            "Rekomendacja: podziel długie komórki "
            "na mniejsze, czytelniejsze fragmenty."
        )
    else:
        print("Długość komórek: OK")

    print("\nAnaliza zagnieżdżenia kodu:")

    for index, cell in enumerate(notebook.cells, start=1):
        if cell.cell_type != "code":
            continue

        depth = calculate_nesting_depth(cell.source)

        if depth is None:
            print(
                f"Komórka {index}: "
                "nie można przeanalizować składni"
            )
            continue

        print(
            f"Komórka {index}: "
            f"poziom zagnieżdżenia = {depth}"
        )

        if depth > 3:
            print(
                "  Rekomendacja: rozważ uproszczenie "
                "zagnieżdżonych instrukcji."
            )

    complexity_score = 100

    complexity_score -= len(long_cells) * 10

    for cell in code_cells:
        depth = calculate_nesting_depth(cell.source)

        if depth is not None and depth > 3:
            complexity_score -= (depth - 3) * 5

    complexity_score = max(0, complexity_score)

    print("\nComplexity Score:")
    print(f"Wynik: {complexity_score}/100")

    unanalyzed_cells = []

    for index, cell in enumerate(notebook.cells, start=1):
        if cell.cell_type != "code":
            continue

        if calculate_nesting_depth(cell.source) is None:
            unanalyzed_cells.append(index)

    if unanalyzed_cells:
        print(
            "UWAGA: Analiza złożoności jest niepełna. "
            f"Nieprzeanalizowane komórki: {unanalyzed_cells}"
        )
        print(
            "Complexity Score nie uwzględnia "
            "zagnieżdżenia w tych komórkach."
        )

    if complexity_score >= 80:
        print("Ocena złożoności: DOBRA")
    elif complexity_score >= 60:
        print("Ocena złożoności: ŚREDNIA")
    else:
        print("Ocena złożoności: WYMAGA POPRAWY")

    print("\nQuality Score:")

    quality_score = 0

    # Dokumentacja: maksymalnie 30 punktów
    if documentation_ok:
        quality_score += 30

    # Markdown na początku: maksymalnie 15 punktów
    if notebook.cells and notebook.cells[0].cell_type == "markdown":
        quality_score += 15

    # Brak pustych komórek: maksymalnie 15 punktów
    if notebook.cells and not empty_cells:
        quality_score += 15

    # Złożoność: maksymalnie 40 punktów
    quality_score += round(complexity_score * 0.4)

    print(f"Wynik końcowy: {quality_score}/100")

    if quality_score >= 80:
        print("Ogólna ocena jakości: DOBRA")
    elif quality_score >= 60:
        print("Ogólna ocena jakości: ŚREDNIA")
    else:
        print("Ogólna ocena jakości: WYMAGA POPRAWY")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
    else:
        notebook_path = "zadanie19/test_good_notebook.ipynb"

    analyze_notebook(notebook_path)
