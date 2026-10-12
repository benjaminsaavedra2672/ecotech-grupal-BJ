from .conexion import abrir_conexion


def crear_tablas():
    conn = abrir_conexion()
    try:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS departamento (
            id_depto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS empleado (
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL UNIQUE,
            departamento_id INTEGER,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            direccion TEXT NOT NULL DEFAULT '',
            telefono TEXT NOT NULL DEFAULT '',
            fecha_contrato TEXT NOT NULL,
            salario REAL NOT NULL CHECK (salario >= 0),
            rol TEXT NOT NULL DEFAULT 'Empleado',
            FOREIGN KEY (usuario_id) REFERENCES usuario(id),
            FOREIGN KEY (departamento_id) REFERENCES departamento(id_depto)
                ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS proyecto (
            id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL DEFAULT '',
            fecha_inicio TEXT NOT NULL DEFAULT '',
            fecha_fin TEXT NOT NULL DEFAULT '',
            CHECK (fecha_fin = '' OR fecha_inicio = '' OR fecha_fin >= fecha_inicio)
        );

        CREATE TABLE IF NOT EXISTS proyecto_empleado (
            proyecto_id INTEGER NOT NULL,
            empleado_id INTEGER NOT NULL,
            PRIMARY KEY (proyecto_id, empleado_id),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS registro_tiempo (
            id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
            empleado_id INTEGER NOT NULL,
            proyecto_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            horas_trabajadas REAL NOT NULL CHECK (horas_trabajadas > 0 AND horas_trabajadas <= 24),
            descripcion_tarea TEXT NOT NULL,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id_proyecto)
        );
        """)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada.")
