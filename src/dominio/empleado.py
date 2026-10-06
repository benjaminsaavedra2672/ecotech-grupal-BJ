#src/dominio/empleado.py
class Empleado:
    def __init__(self, idEmpleado: str, nombre: str, correo: str, direccion: str, telefono: str, fechaContrato: str, salario: str, rol: str,):
        self.idEmpleado = idEmpleado
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.fechaContrato = fechaContrato
        self.salario = salario
        self.rol = rol
    
    def mostrar_datos(self) -> str:
        return f"{self.idEmpleado} - {self.nombre} - {self.correo} - {self.direccion} - {self.telefono} - {self.fechaContrato} - {self.salario} - {self.rol}"

# inicio de segunda clase

class Empleado:
    def calcular_pago(self) -> float:
        raise NotImplementedError

class EmpleadoMensual(Empleado):
    def __init__(self, nombre: str, rut: str, sueldo: float):
        super().__init__(nombre, rut)
        self.sueldo = sueldo

    def calcular_pago(self) -> float:
        return self.sueldo

class EmpleadoPorHora(Empleado):
    def __init__(self, nombre: str, rut: str, horas: float, valor_hora: float):
        super().__init__(nombre, rut)
        self.horas = horas
        self.valor_hora = valor_hora

    def calcular_pago(self) -> float:
        return self.horas * self.valor_hora