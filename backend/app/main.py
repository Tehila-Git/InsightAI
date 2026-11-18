
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.app.data_loader import load_dataset
from backend.app.profiler import profile_dataset


app = FastAPI(
    title="InsightAI API",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/datasets/profile")
async def profile_uploaded_dataset(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in {".csv", ".xlsx"}:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Use CSV or XLSX."
        )

    try:
        content = await file.read()

        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / f"upload{suffix}"
            temp_path.write_bytes(content)

            dataset = load_dataset(temp_path)
            profile = profile_dataset(dataset)

        return profile

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail="Could not process the uploaded file."
        ) from error
