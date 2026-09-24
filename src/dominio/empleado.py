#src/dominio/empleado.py
class Empleado:
    def __init__(self, nombre: str, correo: str):
        self.nombre = nombre
        self.correo = correo
    
    def mostrar_datos(self) -> str:
        return f"{self.nombre} - {self.correo}"

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