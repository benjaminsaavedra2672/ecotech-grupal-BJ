import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _cargar_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


_cargar_env()


def abrir_conexion():
    motor = os.getenv("DB_ENGINE", "sqlite").lower()
    if motor != "sqlite":
        raise ValueError("Esta versión está configurada para SQLite.")
    db_name = os.getenv("DB_NAME", "ecotech.db")
    path = (ROOT / db_name).resolve()
    if ROOT.resolve() not in path.parents and path != ROOT.resolve():
        raise ValueError("La ruta de la base de datos no es válida.")
    conn = sqlite3.connect(path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
