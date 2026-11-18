
from pathlib import Path

import pandas as pd


SUPPORTED_FORMATS = {".csv", ".xlsx"}


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a pandas DataFrame.
    """
    file_path = Path(file_path)

    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    if extension == ".csv":
        dataset = pd.read_csv(file_path)
    else:
        dataset = pd.read_excel(file_path)

    if dataset.empty:
        raise ValueError("The uploaded file contains no data.")

    return dataset
