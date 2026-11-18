
import pandas as pd
import pytest

from backend.app.data_loader import load_dataset


def test_load_csv(tmp_path):
    file_path = tmp_path / "data.csv"

    pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [25, 30]
    }).to_csv(file_path, index=False)

    result = load_dataset(file_path)

    assert len(result) == 2
    assert list(result.columns) == ["name", "age"]
    assert result["age"].tolist() == [25, 30]


def test_load_excel(tmp_path):
    file_path = tmp_path / "data.xlsx"

    pd.DataFrame({
        "score": [85, 90, 95]
    }).to_excel(file_path, index=False)

    result = load_dataset(file_path)

    assert len(result) == 3
    assert result["score"].tolist() == [85, 90, 95]


def test_unsupported_file_format(tmp_path):
    file_path = tmp_path / "data.txt"
    file_path.write_text("some data")

    with pytest.raises(ValueError, match="Unsupported file format"):
        load_dataset(file_path)


def test_empty_dataset(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("name,age\n")

    with pytest.raises(ValueError, match="contains no data"):
        load_dataset(file_path)
