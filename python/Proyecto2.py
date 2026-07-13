import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional

class Empleado:
    def __init__(self, id_empleado: int, nombre: str, puesto: str, salario_base: float, 
                fecha_contratacion: str, departamento: str):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.puesto = puesto
        self.salario_base = salario_base
        self.fecha_contratacion = fecha_contratacion
        self.departamento = departamento
        self.horas_extras = 0
        self.faltas = 0
        self.bonificaciones = 0
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id_empleado,
            'nombre': self.nombre,
            'puesto': self.puesto,
            'salario_base': self.salario_base,
            'fecha_contratacion': self.fecha_contratacion,
            'departamento': self.departamento,
            'horas_extras': self.horas_extras,
            'faltas': self.faltas,
            'bonificaciones': self.bonificaciones
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        empleado = cls(
            data['id'], data['nombre'], data['puesto'],
            data['salario_base'], data['fecha_contratacion'], data['departamento']
        )
        empleado.horas_extras = data.get('horas_extras', 0)
        empleado.faltas = data.get('faltas', 0)
        empleado.bonificaciones = data.get('bonificaciones', 0)
        return empleado

class Nomina:
    def __init__(self, empleado: Empleado, mes: int, año: int):
        self.empleado = empleado
        self.mes = mes
        self.año = año
    
    def calcular_salario(self) -> Dict:
        # Constantes
        valor_hora_normal = self.empleado.salario_base / 160  # 160 horas mensuales
        valor_hora_extra = valor_hora_normal * 1.75  # 75% extra
        descuento_falta = valor_hora_normal * 8  # Descuento por día de falta
        
        # Cálculos
        salario_base = self.empleado.salario_base
        pago_horas_extras = self.empleado.horas_extras * valor_hora_extra
        descuento_faltas = self.empleado.faltas * descuento_falta
        bonificaciones = self.empleado.bonificaciones
        
        salario_bruto = salario_base + pago_horas_extras + bonificaciones - descuento_faltas
        
        # Deducciones (ejemplo típico en México)
        iva_retenido = salario_bruto * 0.16
        isr = self.calcular_isr(salario_bruto)
        seguro_social = salario_bruto * 0.05
        
        total_deducciones = iva_retenido + isr + seguro_social
        salario_neto = salario_bruto - total_deducciones
        
        return {
            'salario_base': salario_base,
            'horas_extras': pago_horas_extras,
            'bonificaciones': bonificaciones,
            'descuento_faltas': descuento_faltas,
            'salario_bruto': salario_bruto,
            'isr': isr,
            'iva_retenido': iva_retenido,
            'seguro_social': seguro_social,
            'total_deducciones': total_deducciones,
            'salario_neto': salario_neto
        }
    
    def calcular_isr(self, salario_bruto: float) -> float:
        """Cálculo simplificado de ISR (impuesto sobre la renta)"""
        if salario_bruto <= 6000:
            return 0
        elif salario_bruto <= 15000:
            return salario_bruto * 0.10
        elif salario_bruto <= 30000:
            return salario_bruto * 0.15
        else:
            return salario_bruto * 0.20
    
    def generar_recibo(self) -> str:
        calculos = self.calcular_salario()
        nombre_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        recibo = f"""
        ================================================
                RECIBO DE NÓMINA
        ================================================
        Empleado: {self.empleado.nombre}
        ID: {self.empleado.id_empleado}
        Puesto: {self.empleado.puesto}
        Departamento: {self.empleado.departamento}
        Periodo: {nombre_meses[self.mes-1]} {self.año}
        ================================================
        
        PERCEPCIONES:
        Salario Base: ${calculos['salario_base']:,.2f}
        Horas Extra: ${calculos['horas_extras']:,.2f}
        Bonificaciones: ${calculos['bonificaciones']:,.2f}
        
        DEDUCCIONES:
        Faltas: -${calculos['descuento_faltas']:,.2f}
        ISR: -${calculos['isr']:,.2f}
        IVA Retenido: -${calculos['iva_retenido']:,.2f}
        Seguro Social: -${calculos['seguro_social']:,.2f}
        
        ================================================
        SALARIO BRUTO: ${calculos['salario_bruto']:,.2f}
        TOTAL DEDUCCIONES: -${calculos['total_deducciones']:,.2f}
        SALARIO NETO: ${calculos['salario_neto']:,.2f}
        ================================================
        """
        return recibo

class SistemaNomina:
    def __init__(self, archivo_datos: str = "empleados.json"):
        self.archivo_datos = archivo_datos
        self.empleados: Dict[int, Empleado] = {}
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar empleados desde archivo JSON"""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    for emp_data in datos:
                        empleado = Empleado.from_dict(emp_data)
                        self.empleados[empleado.id_empleado] = empleado
            except:
                print("Error al cargar datos")
    
    def guardar_datos(self):
        """Guardar empleados en archivo JSON"""
        datos = [emp.to_dict() for emp in self.empleados.values()]
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def agregar_empleado(self, empleado: Empleado):
        if empleado.id_empleado in self.empleados:
            print(f"Error: Ya existe un empleado con ID {empleado.id_empleado}")
            return False
        self.empleados[empleado.id_empleado] = empleado
        self.guardar_datos()
        print(f"Empleado {empleado.nombre} agregado exitosamente")
        return True
    
    def eliminar_empleado(self, id_empleado: int):
        if id_empleado in self.empleados:
            nombre = self.empleados[id_empleado].nombre
            del self.empleados[id_empleado]
            self.guardar_datos()
            print(f"Empleado {nombre} eliminado")
            return True
        print(f"No se encontró empleado con ID {id_empleado}")
        return False
    
    def buscar_empleado(self, id_empleado: int) -> Optional[Empleado]:
        return self.empleados.get(id_empleado)
    
    def listar_empleados(self):
        if not self.empleados:
            print("No hay empleados registrados")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<6} {'Nombre':<25} {'Puesto':<20} {'Departamento':<15} {'Salario Base':>12}")
        print("="*80)
        for emp in self.empleados.values():
            print(f"{emp.id_empleado:<6} {emp.nombre:<25} {emp.puesto:<20} "
                f"{emp.departamento:<15} ${emp.salario_base:>10,.2f}")
        print("="*80)
    
    def actualizar_horas_extras(self, id_empleado: int, horas: float):
        empleado = self.buscar_empleado(id_empleado)
        if empleado:
            empleado.horas_extras = horas
            self.guardar_datos()
            print(f"Horas extras actualizadas: {horas} horas")
    
    def actualizar_faltas(self, id_empleado: int, faltas: int):
        empleado = self.buscar_empleado(id_empleado)
        if empleado:
            empleado.faltas = faltas
            self.guardar_datos()
            print(f"Faltas actualizadas: {faltas} días")
    
    def actualizar_bonificaciones(self, id_empleado: int, bonificacion: float):
        empleado = self.buscar_empleado(id_empleado)
        if empleado:
            empleado.bonificaciones = bonificacion
            self.guardar_datos()
            print(f"Bonificación actualizada: ${bonificacion:,.2f}")
    
    def generar_nomina(self, id_empleado: int, mes: int, año: int):
        empleado = self.buscar_empleado(id_empleado)
        if not empleado:
            print(f"No se encontró empleado con ID {id_empleado}")
            return
        
        nomina = Nomina(empleado, mes, año)
        recibo = nomina.generar_recibo()
        
        # Guardar recibo en archivo
        nombre_archivo = f"recibo_{empleado.id_empleado}_{año}_{mes:02d}.txt"
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(recibo)
        
        print(recibo)
        print(f"\nRecibo guardado en: {nombre_archivo}")
    
    def generar_nominas_mes(self, mes: int, año: int):
        if not self.empleados:
            print("No hay empleados registrados")
            return
        
        print(f"\n{'='*50}")
        print(f"GENERANDO NÓMINAS PARA {mes}/{año}")
        print(f"{'='*50}")
        
        for empleado in self.empleados.values():
            print(f"\nProcesando: {empleado.nombre}")
            self.generar_nomina(empleado.id_empleado, mes, año)

def menu():
    sistema = SistemaNomina()
    
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE NÓMINA Y GESTIÓN DE PERSONAL")
        print("="*50)
        print("1. Agregar empleado")
        print("2. Listar empleados")
        print("3. Buscar empleado")
        print("4. Eliminar empleado")
        print("5. Actualizar horas extras")
        print("6. Actualizar faltas")
        print("7. Actualizar bonificaciones")
        print("8. Generar nómina individual")
        print("9. Generar nómina mensual (todos)")
        print("10. Salir")
        print("="*50)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n--- AGREGAR EMPLEADO ---")
            try:
                id_emp = int(input("ID del empleado: "))
                nombre = input("Nombre completo: ")
                puesto = input("Puesto: ")
                salario = float(input("Salario base: "))
                fecha = input("Fecha de contratación (YYYY-MM-DD): ")
                depto = input("Departamento: ")
                
                empleado = Empleado(id_emp, nombre, puesto, salario, fecha, depto)
                sistema.agregar_empleado(empleado)
            except Exception as e:
                print(f"Error: {e}")
        
        elif opcion == "2":
            sistema.listar_empleados()
        
        elif opcion == "3":
            id_emp = int(input("ID del empleado: "))
            empleado = sistema.buscar_empleado(id_emp)
            if empleado:
                print(f"\nInformación del empleado:")
                print(f"ID: {empleado.id_empleado}")
                print(f"Nombre: {empleado.nombre}")
                print(f"Puesto: {empleado.puesto}")
                print(f"Salario: ${empleado.salario_base:,.2f}")
                print(f"Fecha contratación: {empleado.fecha_contratacion}")
                print(f"Departamento: {empleado.departamento}")
                print(f"Horas extras: {empleado.horas_extras}")
                print(f"Faltas: {empleado.faltas}")
                print(f"Bonificaciones: ${empleado.bonificaciones:,.2f}")
        
        elif opcion == "4":
            id_emp = int(input("ID del empleado a eliminar: "))
            sistema.eliminar_empleado(id_emp)
        
        elif opcion == "5":
            id_emp = int(input("ID del empleado: "))
            horas = float(input("Horas extras del mes: "))
            sistema.actualizar_horas_extras(id_emp, horas)
        
        elif opcion == "6":
            id_emp = int(input("ID del empleado: "))
            faltas = int(input("Número de faltas: "))
            sistema.actualizar_faltas(id_emp, faltas)
        
        elif opcion == "7":
            id_emp = int(input("ID del empleado: "))
            bonus = float(input("Monto de bonificación: "))
            sistema.actualizar_bonificaciones(id_emp, bonus)
        
        elif opcion == "8":
            id_emp = int(input("ID del empleado: "))
            mes = int(input("Mes (1-12): "))
            año = int(input("Año: "))
            sistema.generar_nomina(id_emp, mes, año)
        
        elif opcion == "9":
            mes = int(input("Mes (1-12): "))
            año = int(input("Año: "))
            sistema.generar_nominas_mes(mes, año)
        
        elif opcion == "10":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu()