import ast

def calculate_energy(
    power_watts: float,
    runtime_minutes: float,
    utilization: float = 100.0,
) -> float:
    """
    Oblicza szacowane zużycie energii w kWh.

    Args:
        power_watts: Moc urządzenia w watach.
        runtime_minutes: Czas pracy w minutach.
        utilization: Przyjęty procent wykorzystania mocy.

    Returns:
        Szacowane zużycie energii w kWh.
    """
    if power_watts < 0:
        raise ValueError("Moc nie może być ujemna.")

    if runtime_minutes < 0:
        raise ValueError("Czas pracy nie może być ujemny.")

    if not 0 <= utilization <= 100:
        raise ValueError("Wykorzystanie musi wynosić od 0 do 100%.")

    runtime_hours = runtime_minutes / 60
    effective_power = power_watts * utilization / 100

    energy_kwh = effective_power * runtime_hours / 1000

    return energy_kwh

def calculate_carbon_footprint(
    energy_kwh: float,
    emission_factor: float = 600.0,
) -> float:
    """
    Oblicza szacowany ślad węglowy w gramach CO2e.

    Args:
        energy_kwh: Zużycie energii w kWh.
        emission_factor: Emisyjność energii w g CO2e/kWh.
            Domyślnie 600 jako przykładowe założenie symulacji.

    Returns:
        Szacowana emisja w gramach CO2e.
    """
    if energy_kwh < 0:
        raise ValueError("Zużycie energii nie może być ujemne.")

    if emission_factor < 0:
        raise ValueError("Współczynnik emisji nie może być ujemny.")

    return energy_kwh * emission_factor

def analyze_notebook_code(code_cells: list) -> list[str]:
    """
    Analizuje kod komórek notebooka bez jego wykonywania.

    Zwraca listę sugestii optymalizacji.
    """
    suggestions = set()

    for cell in code_cells:
        source = cell.source

        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                suggestions.add(
                    "Sprawdź możliwość ograniczenia liczby "
                    "iteracji lub zastosowania operacji wektorowych."
                )

            if isinstance(node, ast.Call):
                function = node.func

                if (
                    isinstance(function, ast.Attribute)
                    and function.attr == "iterrows"
                ):
                    suggestions.add(
                        "Rozważ zastąpienie iterrows() "
                        "operacjami wektorowymi pandas."
                    )

                if (
                    isinstance(function, ast.Name)
                    and function.id == "GridSearchCV"
                ):
                    suggestions.add(
                        "Rozważ RandomizedSearchCV lub "
                        "zmniejszenie liczby kombinacji parametrów."
                    )

    return sorted(suggestions)
