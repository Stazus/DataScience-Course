import nbformat


notebook = nbformat.v4.new_notebook()

notebook.cells = [
    nbformat.v4.new_markdown_cell(
        "# Testowy notebook Google Colab"
    ),

    nbformat.v4.new_code_cell(
        "from google.colab import drive\n"
        "drive.mount('/content/drive')"
    ),

    nbformat.v4.new_code_cell(
        "!pip install pandas numpy matplotlib"
    ),

    nbformat.v4.new_code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt"
    ),

    nbformat.v4.new_code_cell(
        "df = pd.read_csv("
        "'/content/drive/MyDrive/dane.csv'"
        ")\n"
        "print(df.head())"
    )
]

nbformat.write(
    notebook,
    "test_colab.ipynb"
)

print("Utworzono notebook test_colab.ipynb")
