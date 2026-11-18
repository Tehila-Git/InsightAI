
import pandas as pd


def profile_dataset(dataset: pd.DataFrame) -> dict:
    """
    Generate a structural and statistical profile of a dataset.
    """
    if dataset.empty:
        raise ValueError("Cannot profile an empty dataset.")

    columns = {}

    for column in dataset.columns:
        series = dataset[column]

        column_info = {
            "data_type": str(series.dtype),
            "missing_values": int(series.isna().sum()),
            "unique_values": int(series.nunique()),
        }

        if pd.api.types.is_numeric_dtype(series):
            column_info["statistics"] = {
                "mean": float(series.mean()) if not pd.isna(series.mean()) else None,
                "median": float(series.median()) if not pd.isna(series.median()) else None,
                "min": float(series.min()) if not pd.isna(series.min()) else None,
                "max": float(series.max()) if not pd.isna(series.max()) else None,
            }

        columns[str(column)] = column_info

    return {
        "row_count": len(dataset),
        "column_count": len(dataset.columns),
        "columns": columns,
    }
