# Uso desde main.py
desarrollo.agregar_empleado(ana)
    print(desarrollo.cantidad_empleados())

for empleado in desarrollo.empleados:
    print(empleado.mostrar_datos())

# main.py

from persistencia.crear_bd import crear_tablas
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

crear_tablas()
empleado = Empleado(nombre="Ana Pérez", correo="ana@ecotech.cl")

print("Antes:", empleado.id)
# None

EmpleadoDAO.insertar(empleado)

print("Después:", empleado.id)
# id generado por la BD

from dominio.empleado import Empleado
empleado = Empleado(
    nombre="Ana Torres",
    correo="ana.torres@ecotech.cl"
)

print(empleado.mostrar_datos())

# comprobar CREATE + READ desde main.py

from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

empleado = Empleado(
    nombre="Ana Torres",
    correo="ana.torres@ecotech.cl"
)

EmpleadoDAO.insertar(empleado)

encontrado = EmpleadoDAO.buscar_por_id(empleado.id)
print("Encontrado:", encontrado)

print("Listado:")
for item in EmpleadoDAO.listar():
    print(item)
