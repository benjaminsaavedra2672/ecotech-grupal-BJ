from persistencia.conexion import abrir_conexion, obtener_motor

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        sql = f"""
            INSERT INTO empleado (nombre, correo)
            VALUES ({marcador}, {marcador})
        """

        cursor.execute(sql, (empleado.nombre, empleado.correo))
        empleado.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado

# una función interna transforma filas

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            id=fila[0],
            nombre=fila[1],
            correo=fila[2]
        )

    @staticmethod
    def buscar_por_id(id_empleado):
        # ... ejecutar SELECT ...
        if fila is None:
            return None
        return EmpleadoDAO._fila_a_empleado(fila)