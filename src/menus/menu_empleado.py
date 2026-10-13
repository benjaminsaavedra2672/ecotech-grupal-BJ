from getpass import getpass

from .menu_dominio_empleado import crear_empleado_desde_datos
from persistencia.empleado_dao import EmpleadoDAO
from .comun import ejecutar, entero, numero, texto


def menu_empleados():
    while True:
        print("\n-- Empleados --\n1 Registrar\n2 Listar\n3 Buscar\n4 Actualizar\n5 Eliminar\n0 Volver")
        op = input("Opción: ").strip()
        if op == "0":
            return
        if op == "1":
            def registrar():
                e = crear_empleado_desde_datos({
                    "username": texto("Usuario: "),
                    "password": getpass("Contraseña: "),
                    "nombre": texto("Nombre: "),
                    "correo": texto("Correo: "),
                    "direccion": texto("Dirección (opcional): ", True),
                    "telefono": texto("Teléfono (opcional): ", True),
                    "salario": numero("Salario: ", minimo=0),
                    "rol": texto("Rol [Empleado]: ", True) or "Empleado",
                    "departamento_id": None,
                })
                EmpleadoDAO.insertar(e)
                print(f"Empleado creado con ID {e.id_empleado}.")
            ejecutar(registrar)
        elif op == "2":
            def listar():
                empleados = EmpleadoDAO.listar()
                if not empleados:
                    print("No hay empleados registrados.")
                for e in empleados:
                    print(f"{e.id_empleado}: {e.nombre} | {e.correo} | {e.rol} | ${e.salario:.2f}")
            ejecutar(listar)
        elif op == "3":
            def buscar():
                e = EmpleadoDAO.buscar_por_id(entero("ID: "))
                print(f"{e.id_empleado}: {e.nombre} | {e.correo} | salario ${e.salario:.2f}" if e else "No encontrado.")
            ejecutar(buscar)
        elif op == "4":
            def actualizar():
                ident = entero("ID: ")
                e = EmpleadoDAO.buscar_por_id(ident)
                if not e:
                    print("No encontrado.")
                    return
                nombre = texto(f"Nombre [{e.nombre}]: ", True) or e.nombre
                correo = texto(f"Correo [{e.correo}]: ", True) or e.correo
                direccion = texto(f"Dirección [{e.direccion}]: ", True) or e.direccion
                telefono = texto(f"Teléfono [{e.telefono}]: ", True) or e.telefono
                salario_txt = texto(f"Salario [{e.salario}]: ", True)
                salario = float(salario_txt.replace(",", ".")) if salario_txt else float(e.salario)
                if not e.actualizarPerfil(nombre, correo, direccion, telefono):
                    raise ValueError("El perfil no es válido.")
                e.salario = salario
                e.validar()
                print("Actualizado." if EmpleadoDAO.actualizar(e) else "No se realizaron cambios.")
            ejecutar(actualizar)
        elif op == "5":
            def eliminar():
                ident = entero("ID: ")
                if input("Confirmar eliminación (s/n): ").strip().lower() == "s":
                    print("Eliminado." if EmpleadoDAO.eliminar(ident) else "No encontrado.")
            ejecutar(eliminar)
        else:
            print("Opción no válida.")
