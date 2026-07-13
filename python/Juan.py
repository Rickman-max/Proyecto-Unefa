import json

class Empleado:
    def __init__(self, id_empleado, nombre, puesto, salario_base):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.puesto = puesto
        self.salario_base = salario_base

    def calcular_nomina(self, bonificacion=0, deduccion=0):
        return self.salario_base + bonificacion - deduccion

    def to_dict(self):
        return {
            "id": self.id_empleado,
            "nombre": self.nombre,
            "puesto": self.puesto,
            "salario": self.salario_base
        }

class SistemaNomina:
    def __init__(self):
        self.empleados = []
        self.cargar_datos()

    def agregar_empleado(self):
        id_emp = input("ID: ")
        nombre = input("Nombre: ")
        puesto = input("Puesto: ")
        try:
            salario = float(input("Salario base: "))
        except ValueError:
            print("Error: Salario debe ser un numero.")
            return

        empleado = Empleado(id_emp, nombre, puesto, salario)
        self.empleados.append(empleado)
        self.guardar_datos()
        print("Empleado agregado correctamente.\n")

    def listar_empleados(self):
        if not self.empleados:
            print("No hay empleados registrados.\n")
            return

        print("\nLista de empleados:")
        for emp in self.empleados:
            print(f"ID: {emp.id_empleado} | Nombre: {emp.nombre} | Puesto: {emp.puesto} | Salario: {emp.salario_base}")
        print()

    def calcular_nomina(self):
        id_emp = input("Ingrese ID del empleado: ")
        for emp in self.empleados:
            if emp.id_empleado == id_emp:
                try:
                    bono = float(input("Bonificacion: "))
                    deduccion = float(input("Deduccion: "))
                except ValueError:
                    print("Error: Bonificacion y deduccion deben ser numeros.\n")
                    return

                salario_neto = emp.calcular_nomina(bono, deduccion)
                print(f"\nNomina de {emp.nombre}:")
                print(f"Salario base: {emp.salario_base}")
                print(f"Bonificacion: {bono}")
                print(f"Deduccion: {deduccion}")
                print(f"Salario neto: {salario_neto}\n")
                return
        print("Empleado no encontrado.\n")

    def guardar_datos(self):
        data = [emp.to_dict() for emp in self.empleados]
        with open("empleados.json", "w") as f:
            json.dump(data, f, indent=4)

    def cargar_datos(self):
        try:
            with open("empleados.json", "r") as f:
                data = json.load(f)
                for emp in data:
                    self.empleados.append(Empleado(emp["id"], emp["nombre"], emp["puesto"], emp["salario"]))
        except FileNotFoundError:
            pass

def menu():
    sistema = SistemaNomina()
    while True:
        print("====== SISTEMA DE NOMINA ======")
        print("1. Agregar empleado")
        print("2. Listar empleados")
        print("3. Calcular nomina")
        print("4. Salir")

        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            sistema.agregar_empleado()
        elif opcion == "2":
            sistema.listar_empleados()
        elif opcion == "3":
            sistema.calcular_nomina()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion invalida.\n")

if __name__ == "__main__":
    menu()