# src/dominio/departamento.py

#inicio segunda clase

from dominio.empleado import Empleado
    
class Departamento:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._empleados: list[Empleado] = []
    
    def agregar_empleado(self, empleado: Empleado) -> bool:
        if empleado in self._empleados:
            return False

        self._empleados.append(empleado)
        return True

# Dentro de Departamento
    @property
    def empleados(self) -> tuple:
        return tuple(self._empleados)
    
    def cantidad_empleados(self) -> int:
        return len(self._empleados)
         