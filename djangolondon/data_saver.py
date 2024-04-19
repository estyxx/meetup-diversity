import json
import pandas as pd
from pathlib import Path
from datetime import datetime


def save_to_excel(data, filename="events_data"):
    """Saves the data to an Excel file in the output directory with a timestamp."""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    full_path = output_dir / f"{filename}_{now}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(full_path, index=False)

    print(f"Data successfully saved to {full_path}.")


def save_to_json(data, filename="events_data"):
    """Saves the data to a JSON file in the output directory with a timestamp."""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    full_path = output_dir / f"{filename}_{now}.json"
    with full_path.open("w") as f:
        json.dump(data, f, indent=2)

    print(f"Data successfully saved to {full_path}.")
