"""
Zadanie 17 - Smart Dependency Manager

Analiza zaleznosci w plikach Jupyter Notebook.
"""

import ast
import json
from pathlib import Path
from importlib import metadata
import subprocess
import sys


def load_notebook(notebook_path):
    """
    Wczytuje plik Jupyter Notebook i zwraca jego komorki.
    """
    path = Path(notebook_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Nie znaleziono notebooka: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        notebook = json.load(file)

    return notebook.get("cells", [])


def extract_imports(cells):
    """
    Wykrywa importy w komorkach kodu Jupyter Notebook.
    Pomija specjalne polecenia Jupytera.
    """
    imports = set()

    for cell in cells:
        if cell.get("cell_type") != "code":
            continue

        source = cell.get("source", [])
        code = "".join(source) if isinstance(source, list) else source

        # Pomijamy komorki wykonywane przez inne interpretery.
        if code.lstrip().startswith("%%"):
            continue

        cleaned_lines = []


        for line in code.splitlines():
            stripped = line.lstrip()

            if stripped.startswith(("%", "!", "?")):
                cleaned_lines.append("pass")
            else:
                cleaned_lines.append(line)

        cleaned_code = "\n".join(cleaned_lines)

        try:
            tree = ast.parse(cleaned_code)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    package = alias.name.split(".")[0]
                    imports.add(package)

            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    package = node.module.split(".")[0]
                    imports.add(package)

    return sorted(imports)

def check_installed_packages(imports):
    """
    Sprawdza, czy importowane moduly maja zainstalowane pakiety.
    Zwraca nazwy pakietow i ich wersje.
    """
    results = []

    package_mapping = metadata.packages_distributions()

    for module in imports:
        if module in sys.stdlib_module_names:
            results.append({
                "module": module,
                "package": None,
                "version": None,
                "status": "Biblioteka standardowa"
            })
            continue

        distributions = package_mapping.get(module, [])


        if not distributions:
            results.append({
                "module": module,
                "package": None,
                "version": None,
                "status": "Nie znaleziono pakietu"
            })
            continue

        for package in distributions:
            try:
                version = metadata.version(package)
                status = "Zainstalowany"
            except metadata.PackageNotFoundError:
                version = None
                status = "Nie znaleziono pakietu"

            results.append({
                "module": module,
                "package": package,
                "version": version,
                "status": status
            })

    return results

def generate_requirements(packages, output_path="requirements_zadanie17.txt"):
    """
    Generuje minimalny plik requirements.txt
    na podstawie wykrytych pakietow.
    """
    requirements = set()

    for item in packages:
        package = item["package"]
        version = item["version"]

        if package and version:
            requirements.add(f"{package}=={version}")

    requirements = sorted(requirements)

    with open(output_path, "w", encoding="utf-8") as file:
        for requirement in requirements:
            file.write(requirement + "\n")

    return requirements

def check_dependency_conflicts():
    """
    Sprawdza konflikty zaleznosci w aktywnym
    srodowisku Pythona za pomoca pip check.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        capture_output=True,
        text=True,
        check=False
    )

    output = (result.stdout + result.stderr).strip()

    return {
        "status": "OK" if result.returncode == 0 else "PROBLEM",
        "return_code": result.returncode,
        "details": output
    }

def suggest_alternatives(imports):
    """
    Proponuje alternatywne biblioteki
    dla wybranych importowanych modulow.
    """
    alternatives = {
        "pandas": (
            "polars",
            "Alternatywa do przetwarzania danych tabelarycznych. "
            "Moze byc szybsza w wybranych operacjach."
        ),
        "matplotlib": (
            "plotext",
            "Biblioteka do prostych wykresow w terminalu. "
            "Nie zastapi wszystkich funkcji Matplotlib."
        ),
        "requests": (
            "urllib.request",
            "Modul standardowej biblioteki Pythona. "
            "Nie wymaga instalacji dodatkowego pakietu."
        ),
        "bs4": (
            "selectolax",
            "Alternatywa do parsowania HTML, "
            "ktora moze byc szybsza w wybranych zastosowaniach."
        ),
    }

    suggestions = []

    for module in imports:
        if module in alternatives:
            alternative, reason = alternatives[module]

            suggestions.append({
                "module": module,
                "alternative": alternative,
                "reason": reason
            })

    return suggestions

def generate_markdown_report(
    notebook_path,
    imports,
    packages,
    conflicts,
    suggestions,
    output_path="dependency_report_zadanie17.md"
):
    """
    Generuje raport Markdown z analizy zaleznosci.
    """
    lines = [
        "# Smart Dependency Manager - raport",
        "",
        f"Analizowany notebook: `{notebook_path}`",
        "",
        "## 1. Wykryte importy",
        "",
    ]

    for module in imports:
        lines.append(f"- `{module}`")


    lines.extend([
        "",
        "## 2. Zainstalowane pakiety",
        "",
        "| Modul | Pakiet | Wersja | Status |",
        "|---|---|---|---|",
    ])

    for item in packages:
        lines.append(
            f"| {item['module']} | {item['package'] or '-'} "
            f"| {item['version'] or '-'} | {item['status']} |"
        )

    lines.extend([
        "",
        "## 3. Kontrola konfliktow zaleznosci",
        "",
        f"**Status:** {conflicts['status']}",
        "",
        f"**Szczegoly:** {conflicts['details']}",
        "",
        "## 4. Sugerowane alternatywy",
        "",
    ])

    if suggestions:
        for item in suggestions:
            lines.extend([
                f"### {item['module']} -> {item['alternative']}",
                "",
                item["reason"],
                "",
            ])
    else:
        lines.append("Brak sugestii alternatywnych bibliotek.")

    missing_packages = [
        item["module"]
        for item in packages
        if item["status"] == "Nie znaleziono pakietu"
    ]

    lines.extend([
        "",
        "## 5. Brakujace biblioteki",
        "",
    ])

    if missing_packages:
        for module in sorted(set(missing_packages)):
            lines.append(
                f"- `{module}` - nie znaleziono pakietu. "
                "Wymagana reczna weryfikacja i instalacja."
            )
    else:
        lines.append("Nie wykryto brakujacych bibliotek.")


    lines.extend([
        "",
        "## 6. Ograniczenia analizy",
        "",
        "- Importy sa analizowane statycznie za pomoca AST.",
        "- Importy dynamiczne moga nie zostac wykryte.",
        "- Kontrola pip check dotyczy aktywnego srodowiska.",
        "- Sugestie alternatyw wymagaja indywidualnej oceny.",
        "",
    ])

    Path(output_path).write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    return output_path

def main():
    """
    Uruchamia pelna analize zaleznosci notebooka.
    """
    if len(sys.argv) != 2:
        print("Uzycie: python zadanie17.py plik.ipynb")
        sys.exit(1)

    notebook_path = sys.argv[1]

    cells = load_notebook(notebook_path)
    imports = extract_imports(cells)
    packages = check_installed_packages(imports)

    requirements = generate_requirements(packages)
    conflicts = check_dependency_conflicts()
    suggestions = suggest_alternatives(imports)

    report_path = generate_markdown_report(
        notebook_path,
        imports,
        packages,
        conflicts,
        suggestions,
        output_path="dependency_report_zadanie17.md"
    )

    print("\n=== SMART DEPENDENCY MANAGER ===")
    print("Notebook:", notebook_path)
    print("Wykryte importy:", len(imports))
    print("Zaleznosci:", len(requirements))
    print("Kontrola konfliktow:", conflicts["status"])
    print("Sugestie alternatyw:", len(suggestions))
    print("\nWygenerowane pliki:")
    print("- requirements_zadanie17.txt")
    print("-", report_path)


if __name__ == "__main__":
    main()
