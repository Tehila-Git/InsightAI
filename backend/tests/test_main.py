
from io import BytesIO

import pandas as pd
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_profile_csv_upload():
    csv_content = b"age,salary\n25,8000\n30,10000\n"

    response = client.post(
        "/datasets/profile",
        files={"file": ("data.csv", BytesIO(csv_content), "text/csv")}
    )

    assert response.status_code == 200

    result = response.json()

    assert result["row_count"] == 2
    assert result["column_count"] == 2
    assert result["columns"]["age"]["statistics"]["mean"] == 27.5


def test_profile_excel_upload():
    excel_buffer = BytesIO()

    pd.DataFrame({
        "age": [25, 30],
        "salary": [8000, 10000]
    }).to_excel(excel_buffer, index=False)

    response = client.post(
        "/datasets/profile",
        files={
            "file": (
                "data.xlsx",
                BytesIO(excel_buffer.getvalue()),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["row_count"] == 2
    assert result["column_count"] == 2
    assert result["columns"]["age"]["statistics"]["mean"] == 27.5

def test_profile_unsupported_file():
    response = client.post(
        "/datasets/profile",
        files={"file": ("data.txt", b"some data", "text/plain")}
    )

    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]


def test_profile_empty_csv():
    response = client.post(
        "/datasets/profile",
        files={"file": ("empty.csv", b"name,age\n", "text/csv")}
    )

    assert response.status_code == 400
