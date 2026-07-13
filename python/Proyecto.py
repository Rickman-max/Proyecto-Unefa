empleado = {
    "nombre": "Juan",
    "tipo_salario": "mensual",
    "sueldo_base": 750,
    "salario_mensual": 750,
    "salario_diario": None  # Se calculará después
}


empleado["salario_diario"] = round(empleado["salario_mensual"] / 30, 2)

def calcular_salario_base(empleado, dias_trabajados=None, horas_trabajadas=None):
    tipo = empleado["tipo_salario"]
    sueldo_base = empleado["sueldo_base"]
    
    if tipo == "mensual":
        salario_diario = sueldo_base / 30
        if dias_trabajados is not None:
            return round(salario_diario * dias_trabajados, 2)
        else:
            return sueldo_base
    
    elif tipo == "por_hora":
        if horas_trabajadas is not None:
            return round(sueldo_base * horas_trabajadas, 2)
        else:
            return 0
    
    elif tipo == "quincenal":
        # Si ya tiene quincena fija
        return sueldo_base
    
    else:
        return 0


print(calcular_salario_base(empleado, dias_trabajados=20))  # Salario por 20 días
print(calcular_salario_base(empleado))  # Salario mensual completo
