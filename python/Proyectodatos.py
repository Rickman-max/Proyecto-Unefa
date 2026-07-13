class Persona:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
    
    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre}"


class Empleado(Persona):
    def __init__(self, id, nombre, puesto, salario):
        super().__init__(id, nombre)
        self.puesto = puesto
        self.salario = salario
    
    def __str__(self):
        return f"ID: {self.id} | {self.nombre} | {self.puesto} | ${self.salario:,.2f}"


class GestionPersonal:
    def __init__(self):
        self.empleados = {}
        self.contador = 1
    
    def agregar(self, nombre, puesto, salario):
        emp = Empleado(self.contador, nombre, puesto, salario)
        self.empleados[self.contador] = emp
        print(f"[OK] Empleado '{nombre}' agregado (ID: {self.contador})")
        self.contador += 1
    
    def ver_todos(self):
        if not self.empleados:
            print("[INFO] No hay empleados")
            return
        print("\n" + "="*50)
        for emp in self.empleados.values():
            print(emp)
        print("="*50)
    
    def buscar(self, id):
        emp = self.empleados.get(id)
        if emp:
            print(emp)
        else:
            print(f"[ERROR] Empleado ID {id} no encontrado")
        return emp
    
    def actualizar(self, id, nombre=None, puesto=None, salario=None):
        emp = self.empleados.get(id)
        if emp:
            if nombre:
                emp.nombre = nombre
            if puesto:
                emp.puesto = puesto
            if salario:
                emp.salario = salario
            print(f"[OK] Empleado ID {id} actualizado")
        else:
            print(f"[ERROR] Empleado ID {id} no encontrado")
    
    def eliminar(self, id):
        emp = self.empleados.pop(id, None)
        if emp:
            print(f"[OK] Empleado '{emp.nombre}' eliminado")
        else:
            print(f"[ERROR] Empleado ID {id} no encontrado")
    
    def menu(self):
        while True:
            print("\n" + "="*40)
            print("1. Agregar empleado")
            print("2. Ver todos")
            print("3. Buscar empleado")
            print("4. Actualizar empleado")
            print("5. Eliminar empleado")
            print("6. Salir")
            print("="*40)
            
            opcion = input("Opcion (1-6): ")
            
            if opcion == "1":
                try:
                    nombre = input("Nombre: ")
                    puesto = input("Puesto: ")
                    salario = float(input("Salario: "))
                    self.agregar(nombre, puesto, salario)
                except ValueError:
                    print("[ERROR] Salario debe ser un numero")
            
            elif opcion == "2":
                self.ver_todos()
            
            elif opcion == "3":
                try:
                    id = int(input("ID: "))
                    self.buscar(id)
                except ValueError:
                    print("[ERROR] ID debe ser un numero")
            
            elif opcion == "4":
                try:
                    id = int(input("ID: "))
                    nombre = input("Nuevo nombre (Enter para omitir): ")
                    puesto = input("Nuevo puesto (Enter para omitir): ")
                    salario_input = input("Nuevo salario (Enter para omitir): ")
                    salario = float(salario_input) if salario_input else None
                    self.actualizar(id, nombre or None, puesto or None, salario)
                except ValueError:
                    print("[ERROR] Datos invalidos")
            
            elif opcion == "5":
                try:
                    id = int(input("ID a eliminar: "))
                    self.eliminar(id)
                except ValueError:
                    print("[ERROR] ID debe ser un numero")
            
            elif opcion == "6":
                print("[OK] Hasta luego!")
                break
            
            else:
                print("[ERROR] Opcion invalida")


if __name__ == "__main__":
    GestionPersonal().menu()