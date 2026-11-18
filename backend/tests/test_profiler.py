
import pandas as pd
import pytest

from backend.app.profiler import profile_dataset


def test_profile_dataset():
    dataset = pd.DataFrame({
        "age": [20, 30, 40],
        "name": ["Alice", "Bob", "Charlie"]
    })

    result = profile_dataset(dataset)

    assert result["row_count"] == 3
    assert result["column_count"] == 2

    assert result["columns"]["age"]["statistics"]["mean"] == 30.0
    assert result["columns"]["age"]["statistics"]["median"] == 30.0
    assert result["columns"]["age"]["statistics"]["min"] == 20.0
    assert result["columns"]["age"]["statistics"]["max"] == 40.0


def test_profile_missing_values():
    dataset = pd.DataFrame({
        "score": [10, None, 30]
    })

    result = profile_dataset(dataset)

    assert result["columns"]["score"]["missing_values"] == 1


def test_profile_empty_dataset():
    dataset = pd.DataFrame()

    with pytest.raises(ValueError, match="empty dataset"):
        profile_dataset(dataset)
