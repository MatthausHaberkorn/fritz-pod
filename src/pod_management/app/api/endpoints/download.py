from pathlib import Path

import duckdb
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
async def download_db():
    db_path = Path("fritzpod.db")  # replace with your actual db path
    if db_path.exists():
        return FileResponse(
            str(db_path), media_type="application/octet-stream", filename=db_path.name
        )
    else:
        raise HTTPException(status_code=404, detail="Database file not found")


class DuckDBConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = duckdb
        self.conn.install_extension("sqlite")
        self.conn.load_extension("sqlite")
        self.conn = duckdb.connect(database=str(self.db_path), read_only=True)

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


@router.get("/{table_name}/{file_format}")
async def get_tables(table_name: str, file_format: str):
    db_path = Path("app/local_db/fritzpod.db")  # replace with your actual db path
    if db_path.exists():
        file_path = Path(f"{table_name}.{file_format}")
        with DuckDBConnection(db_path) as conn:
            if file_format == "csv":
                conn.execute(
                    f"COPY (SELECT * FROM {table_name}) TO '{file_path}' (FORMAT CSV)"
                )
                media_type = "text/csv"
            elif file_format == "parquet":
                conn.execute(
                    f"COPY (SELECT * FROM {table_name}) TO '{file_path}' (FORMAT PARQUET)"
                )
                media_type = "application/octet-stream"
            else:
                raise HTTPException(status_code=400, detail="Invalid format")
        return FileResponse(
            str(file_path),
            media_type=media_type,
            filename=f"{table_name}.{file_format}",
        )
    else:
        raise HTTPException(status_code=404, detail="Database file not found")
