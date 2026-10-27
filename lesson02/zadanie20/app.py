import plotly.graph_objects as go
import streamlit as st
import nbformat

try:
    from .analysis import (
        calculate_energy,
        calculate_carbon_footprint,
        analyze_notebook_code,
    )
    from .report import generate_pdf_report
except ImportError:
    from analysis import (
        calculate_energy,
        calculate_carbon_footprint,
        analyze_notebook_code,
    )
    from report import generate_pdf_report

st.set_page_config(
    page_title="Green Data Science Dashboard",
    page_icon="🌱",
    layout="wide",
)

st.title("🌱 Green Data Science Dashboard")

st.write(
    "Aplikacja do szacowania zużycia energii "
    "i śladu węglowego notebooków Jupyter."
)

st.header("1. Wczytywanie notebooka")

uploaded_file = st.file_uploader(
    "Wybierz plik notebooka Jupyter",
    type=["ipynb"],
)

if uploaded_file is not None:
    try:
        notebook = nbformat.reads(
            uploaded_file.getvalue().decode("utf-8"),
            as_version=4,
        )

        code_cells = [
            cell for cell in notebook.cells
            if cell.cell_type == "code"
        ]

        markdown_cells = [
            cell for cell in notebook.cells
            if cell.cell_type == "markdown"
        ]

        st.success(f"Wczytano plik: {uploaded_file.name}")

        st.subheader("Statystyki notebooka")

        col1, col2, col3 = st.columns(3)

        col1.metric("Wszystkie komórki", len(notebook.cells))
        col2.metric("Komórki kodu", len(code_cells))
        col3.metric("Komórki Markdown", len(markdown_cells))

    except (UnicodeDecodeError, ValueError) as error:
        st.error(f"Nie udało się odczytać notebooka: {error}")

else:
    st.info("Wgraj notebook, aby rozpocząć analizę.")

st.header("2. Symulacja zużycia energii")

st.info(
    "Wyniki są szacunkowe. Aplikacja nie mierzy "
    "rzeczywistego poboru energii przez komputer."
)

col1, col2 = st.columns(2)

with col1:
    power_watts = st.slider(
        "Moc urządzenia (W)",
        min_value=10,
        max_value=500,
        value=200,
        step=10,
    )

    runtime_minutes = st.slider(
        "Czas pracy (minuty)",
        min_value=1,
        max_value=240,
        value=60,
    )

with col2:
    utilization = st.slider(
        "Wykorzystanie przyjętej mocy (%)",
        min_value=0,
        max_value=100,
        value=50,
    )

    emission_factor = st.number_input(
        "Emisyjność energii (g CO₂e/kWh)",
        min_value=0.0,
        max_value=2000.0,
        value=600.0,
        step=10.0,
    )

energy = calculate_energy(
    power_watts,
    runtime_minutes,
    utilization,
)

carbon = calculate_carbon_footprint(
    energy,
    emission_factor,
)

st.subheader("Wyniki symulacji")

result1, result2 = st.columns(2)

result1.metric(
    "Szacowane zużycie energii",
    f"{energy:.4f} kWh",
)

result2.metric(
    "Szacowany ślad węglowy",
    f"{carbon:.2f} g CO₂e",
)

st.header("3. Wizualizacja zużycia zasobów")

gauge1, gauge2 = st.columns(2)

energy_limit = 1.0
carbon_limit = energy_limit * emission_factor

energy_chart = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=energy,
        number={"suffix": " kWh", "valueformat": ".4f"},
        title={"text": "Szacowane zużycie energii"},
        gauge={
            "axis": {"range": [0, max(energy_limit, energy * 1.2)]},
            "bar": {"color": "green"},
            "steps": [
                {"range": [0, 0.3], "color": "#d8f3dc"},
                {"range": [0.3, 0.7], "color": "#fff3bf"},
                {"range": [0.7, 1.0], "color": "#ffe3e3"},
            ],
        },
    )
)

carbon_chart = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=carbon,
        number={"suffix": " g CO₂e", "valueformat": ".2f"},
        title={"text": "Szacowany ślad węglowy"},
        gauge={
            "axis": {"range": [0, max(carbon_limit, carbon * 1.2, 1)]},
            "bar": {"color": "darkorange"},
        },
    )
)

gauge1.plotly_chart(energy_chart, use_container_width=True)
gauge2.plotly_chart(carbon_chart, use_container_width=True)

st.caption(
    "Skale wykresów są orientacyjne i nie stanowią "
    "norm środowiskowych."
)

st.header("4. Porównanie scenariuszy")

st.write(
    "Porównaj aktualne założenia z wariantem, "
    "w którym obliczenia trwają krócej."
)

optimization_percent = st.slider(
    "Zakładane skrócenie czasu obliczeń (%)",
    min_value=0,
    max_value=90,
    value=30,
    step=5,
)

optimized_runtime = runtime_minutes * (
    1 - optimization_percent / 100
)

optimized_energy = calculate_energy(
    power_watts,
    optimized_runtime,
    utilization,
)

optimized_carbon = calculate_carbon_footprint(
    optimized_energy,
    emission_factor,
)

energy_savings = energy - optimized_energy
carbon_savings = carbon - optimized_carbon

comparison_chart = go.Figure()

comparison_chart.add_trace(
    go.Bar(
        name="Scenariusz podstawowy",
        x=["Zużycie energii (kWh)"],
        y=[energy],
    )
)

comparison_chart.add_trace(
    go.Bar(
        name="Scenariusz zoptymalizowany",
        x=["Zużycie energii (kWh)"],
        y=[optimized_energy],
    )
)

comparison_chart.update_layout(
    title="Porównanie zużycia energii",
    barmode="group",
    yaxis_title="Energia (kWh)",
)

st.plotly_chart(
    comparison_chart,
    use_container_width=True,
)

savings_col1, savings_col2 = st.columns(2)

savings_col1.metric(
    "Potencjalna oszczędność energii",
    f"{energy_savings:.4f} kWh",
)

savings_col2.metric(
    "Potencjalna redukcja emisji",
    f"{carbon_savings:.2f} g CO₂e",
)

st.caption(
    "Scenariusz zoptymalizowany zakłada skrócenie "
    "czasu pracy przy niezmienionej mocy i wykorzystaniu. "
    "Nie jest to gwarantowana oszczędność."
)

st.header("5. Sugestie optymalizacji kodu")

if uploaded_file is not None:
    try:
        notebook = nbformat.reads(
            uploaded_file.getvalue().decode("utf-8"),
            as_version=4,
        )

        code_cells = [
            cell for cell in notebook.cells
            if cell.cell_type == "code"
        ]

        suggestions = analyze_notebook_code(code_cells)

        if suggestions:
            st.warning(
                f"Wykryto {len(suggestions)} "
                "potencjalnych obszarów optymalizacji."
            )

            for number, suggestion in enumerate(
                suggestions, start=1
            ):
                st.write(f"{number}. {suggestion}")
        else:
            st.success(
                "Nie wykryto problemów objętych "
                "podstawową analizą statyczną."
            )

        st.caption(
            "Sugestie wynikają z analizy składni kodu. "
            "Nie potwierdzają rzeczywistego zużycia zasobów."
        )

    except (UnicodeDecodeError, ValueError) as error:
        st.error(f"Błąd analizy notebooka: {error}")

else:
    st.info(
        "Wgraj notebook Jupyter, aby otrzymać "
        "sugestie optymalizacji kodu."
    )

st.header("6. Eksport raportu PDF")

if uploaded_file is not None:
    try:
        pdf_data = generate_pdf_report(
            notebook_name=uploaded_file.name,
            energy_kwh=energy,
            carbon_g=carbon,
            optimized_energy_kwh=optimized_energy,
            optimized_carbon_g=optimized_carbon,
            suggestions=suggestions,
        )

        st.download_button(
            label="📄 Pobierz raport PDF",
            data=pdf_data,
            file_name="green_data_science_report.pdf",
            mime="application/pdf",
        )

    except Exception as error:
        st.error(f"Nie udało się wygenerować raportu: {error}")

else:
    st.info(
        "Wgraj notebook Jupyter, aby pobrać raport PDF."
    )
