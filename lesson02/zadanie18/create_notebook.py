import nbformat
from pathlib import Path

notebook = nbformat.v4.new_notebook()

notebook.cells = [
    nbformat.v4.new_code_cell(
        """import sys
import platform

print("Python:", sys.version.split()[0])
print("System:", platform.system())"""
    ),
    nbformat.v4.new_code_cell(
        """numbers = list(range(1, 10001))

result = {
    "sum": sum(numbers),
    "count": len(numbers),
    "squares_sum": sum(x * x for x in numbers),
}

print(result)"""
    ),
    nbformat.v4.new_code_cell(
        """import hashlib
import json

data = json.dumps(result, sort_keys=True)
checksum = hashlib.sha256(data.encode()).hexdigest()

print("SHA256:", checksum)"""
    ),
]

output_path = Path(__file__).parent / "test_notebook.ipynb"

nbformat.write(notebook, output_path)

print(f"Utworzono notebook: {output_path}")
