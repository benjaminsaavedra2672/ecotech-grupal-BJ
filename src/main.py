from getpass import getpass

from dominio.empleado import Empleado
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO


def texto(mensaje, permitir_vacio=False):
    valor = input(mensaje).strip()
    if not valor and not permitir_vacio:
        raise ValueError("El campo no puede estar vacío.")
    return valor


def entero(mensaje):
    valor = int(input(mensaje))
    if valor <= 0:
        raise ValueError("Debe ingresar un entero mayor que cero.")
    return valor


def numero(mensaje):
    valor = float(input(mensaje))
    if valor < 0:
        raise ValueError("El número no puede ser negativo.")
    return valor


def ejecutar(accion):
    try:
        accion()
    except ValueError as exc:
        print(f"Datos inválidos: {exc}")
    except Exception as exc:
        print(f"Operación fallida: {exc}")


def menu_empleados():
    while True:
        print("\n-- Empleados --\n1 Registrar\n2 Listar\n3 Buscar\n4 Actualizar\n5 Eliminar\n0 Volver")
        op = input("Opción: ").strip()
        if op == "0":
            return
        if op == "1":
            def registrar():
                e = Empleado(
                    username=texto("Usuario: "),
                    password=getpass("Contraseña: "),
                    nombre=texto("Nombre: "),
                    correo=texto("Correo: "),
                    direccion=texto("Dirección (opcional): ", True),
                    telefono=texto("Teléfono (opcional): ", True),
                    salario=numero("Salario: "),
                    rol=texto("Rol [Empleado]: ", True) or "Empleado",
                    departamento_id=None
                )
                EmpleadoDAO.insertar(e)
                print(f"Empleado creado con ID {e.id_empleado}.")
            ejecutar(registrar)
        elif op == "2":
            ejecutar(lambda: [
                print(f'{e.id_empleado}: {e.nombre} | {e.correo} | {e.rol} | ${e.salario:.2f}')
                for e in EmpleadoDAO.listar()
            ])
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
                salario = numero(f"Salario [{e.salario}]: ")
                if not e.actualizarPerfil(nombre, correo, direccion, telefono):
                    raise ValueError("Perfil no válido.")
                e.salario = salario
                print("Actualizado." if EmpleadoDAO.actualizar(e) else "Sin cambios.")
            ejecutar(actualizar)
        elif op == "5":
            def eliminar():
                ident = entero("ID: ")
                if input("Confirmar eliminación (s/n): ").strip().lower() == "s":
                    print("Eliminado." if EmpleadoDAO.eliminar(ident) else "No encontrado.")
            ejecutar(eliminar)
        else:
            print("Opción no válida.")


def menu_departamentos():
    while True:
        print("\n-- Departamentos --\n1 Crear\n2 Listar\n3 Actualizar\n4 Eliminar\n0 Volver")
        op = input("Opción: ").strip()
        if op == "0": return
        if op == "1":
            ejecutar(lambda: print(f"Departamento creado con ID {DepartamentoDAO.insertar(texto('Nombre: '))}."))
        elif op == "2":
            ejecutar(lambda: [print(f"{r['id_depto']}: {r['nombre']} | empleados: {r['empleados']}") for r in DepartamentoDAO.listar()])
        elif op == "3":
            def upd():
                ident = entero("ID: ")
                print("Actualizado." if DepartamentoDAO.actualizar(ident, texto("Nuevo nombre: ")) else "No encontrado.")
            ejecutar(upd)
        elif op == "4":
            ejecutar(lambda: print("Eliminado." if DepartamentoDAO.eliminar(entero("ID: ")) else "No encontrado."))
        else: print("Opción no válida.")


def menu_proyectos():
    while True:
        print("\n-- Proyectos --\n1 Crear\n2 Listar\n3 Actualizar\n4 Eliminar\n5 Asignar empleado\n0 Volver")
        op = input("Opción: ").strip()
        if op == "0": return
        if op == "1":
            def crear():
                ident = ProyectoDAO.insertar(texto("Nombre: "), texto("Descripción: ", True),
                    texto("Fecha inicio AAAA-MM-DD (opcional): ", True),
                    texto("Fecha fin AAAA-MM-DD (opcional): ", True))
                print(f"Proyecto creado con ID {ident}.")
            ejecutar(crear)
        elif op == "2":
            ejecutar(lambda: [print(f"{r['id_proyecto']}: {r['nombre']} | {r['fecha_inicio']} - {r['fecha_fin']}") for r in ProyectoDAO.listar()])
        elif op == "3":
            def upd():
                ident = entero("ID: ")
                row = ProyectoDAO.buscar_por_id(ident)
                if not row: print("No encontrado."); return
                print("Actualizado." if ProyectoDAO.actualizar(ident,
                    texto(f"Nombre [{row['nombre']}]: ", True) or row['nombre'],
                    texto(f"Descripción [{row['descripcion']}]: ", True) or row['descripcion'],
                    texto(f"Inicio [{row['fecha_inicio']}]: ", True) or row['fecha_inicio'],
                    texto(f"Fin [{row['fecha_fin']}]: ", True) or row['fecha_fin']) else "No encontrado.")
            ejecutar(upd)
        elif op == "4":
            ejecutar(lambda: print("Eliminado." if ProyectoDAO.eliminar(entero("ID: ")) else "No encontrado."))
        elif op == "5":
            ejecutar(lambda: (ProyectoDAO.asignar_empleado(entero("ID proyecto: "), entero("ID empleado: ")), print("Empleado asignado.")))
        else: print("Opción no válida.")


def menu_registros():
    while True:
        print("\n-- Registros de tiempo --\n1 Crear\n2 Listar\n3 Eliminar\n0 Volver")
        op = input("Opción: ").strip()
        if op == "0": return
        if op == "1":
            def crear():
                ident = RegistroTiempoDAO.insertar(
                    entero("ID empleado: "), entero("ID proyecto: "),
                    texto("Fecha AAAA-MM-DD: "), float(input("Horas (0-24): ")),
                    texto("Descripción de tarea: "))
                print(f"Registro creado con ID {ident}.")
            ejecutar(crear)
        elif op == "2":
            ejecutar(lambda: [print(f"{r['id_registro']}: {r['fecha']} | {r['empleado']} | {r['proyecto']} | {r['horas_trabajadas']} h | {r['descripcion_tarea']}") for r in RegistroTiempoDAO.listar()])
        elif op == "3":
            ejecutar(lambda: print("Eliminado." if RegistroTiempoDAO.eliminar(entero("ID registro: ")) else "No encontrado."))
        else: print("Opción no válida.")


def main():
    try:
        crear_tablas()
    except Exception as exc:
        print(f"No se pudo inicializar la base de datos: {exc}")
        return
    while True:
        print("\n=== ECOTECH SOLUTIONS ===\n1 Empleados\n2 Departamentos\n3 Proyectos\n4 Registros de tiempo\n0 Salir")
        op = input("Opción: ").strip()
        if op == "1": menu_empleados()
        elif op == "2": menu_departamentos()
        elif op == "3": menu_proyectos()
        elif op == "4": menu_registros()
        elif op == "0":
            print("Hasta luego.")
            break
        else: print("Opción no válida.")


if __name__ == "__main__":
    main()
