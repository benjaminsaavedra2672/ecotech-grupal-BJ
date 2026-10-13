"""Conexión configurable a SQLite o MySQL mediante variables de entorno."""
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _cargar_env():
    """Carga un .env sencillo sin depender de paquetes externos."""
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(
                    key.strip(),
                    value.strip().strip('"').strip("'")
                )


_cargar_env()


def motor_actual():
    return os.getenv("DB_ENGINE", "sqlite").strip().lower()


class CursorMySQL:
    """Envuelve el cursor para traducir los marcadores de parámetros."""

    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, sql, parametros=()):
        self._cursor.execute(ConexionMySQL._sql(sql), parametros)
        return self

    def __getattr__(self, nombre):
        return getattr(self._cursor, nombre)


class ConexionMySQL:
    """Adaptador para mantener compatibles los DAO escritos con estilo sqlite3."""

    def __init__(self, conexion):
        self._conexion = conexion

    @staticmethod
    def _sql(sql):
        # Los DAO usan '?' y MySQL utiliza '%s'.
        return sql.replace("?", "%s")

    def execute(self, sql, parametros=()):
        cursor = self._conexion.cursor(dictionary=True)
        cursor.execute(self._sql(sql), parametros)
        return cursor

    def cursor(self):
        return CursorMySQL(self._conexion.cursor(dictionary=True))

    def executescript(self, script):
        cursor = self._conexion.cursor()
        try:
            for sentencia in script.split(";"):
                sentencia = sentencia.strip()
                if sentencia:
                    cursor.execute(sentencia)
        finally:
            cursor.close()

    def commit(self):
        self._conexion.commit()

    def rollback(self):
        self._conexion.rollback()

    def close(self):
        self._conexion.close()


def abrir_conexion():
    motor = motor_actual()

    if motor == "sqlite":
        db_name = os.getenv("DB_NAME", "ecotech.db")
        path = (ROOT / db_name).resolve()

        if ROOT.resolve() not in path.parents and path != ROOT.resolve():
            raise ValueError("La ruta de la base de datos no es válida.")

        conn = sqlite3.connect(path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    if motor == "mysql":
        try:
            import mysql.connector
        except ImportError as exc:
            raise RuntimeError(
                "Falta el conector MySQL. Ejecuta: "
                "py -m pip install mysql-connector-python"
            ) from exc

        # DB_PASSWORD puede estar vacío si MySQL no tiene contraseña.
        requeridas = ("DB_HOST", "DB_NAME", "DB_USER")
        faltantes = [
            nombre
            for nombre in requeridas
            if os.getenv(nombre) is None or not os.getenv(nombre).strip()
        ]

        # Solo comprobamos que DB_PASSWORD exista; aceptamos una cadena vacía.
        if os.getenv("DB_PASSWORD") is None:
            faltantes.append("DB_PASSWORD")

        if faltantes:
            raise ValueError(
                "Faltan variables en .env: " + ", ".join(faltantes)
            )

        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            database=os.getenv("DB_NAME", "ecotech"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD", ""),
            connection_timeout=10,
            charset="utf8mb4",
            use_unicode=True,
        )

        return ConexionMySQL(conexion)

    raise ValueError("DB_ENGINE debe ser 'sqlite' o 'mysql'.")