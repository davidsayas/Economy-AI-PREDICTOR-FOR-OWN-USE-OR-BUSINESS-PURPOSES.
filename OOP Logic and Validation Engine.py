import datetime

class Transaccion:
 #I created a class with some inside validations to verify that the data registried by the user is clean
    def __init__(self, monto, concepto: str, categoria: str, tipo: str):
        self.monto = self._validar_monto(monto) 
        self.concepto = self._validar_texto(concepto, "concepto") # 
        self.categoria = self._validar_texto(categoria, "categoria")
        self.tipo = self._validar_tipo(tipo)
        self.fecha = datetime.date.today()

    #First validation of private method, to rectified if the value registried by the user is correct.
    def _validar_monto(self, monto) -> float:
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError("El monto debe ser un numero mayor a cero")
            return monto_float
        except ValueError as e:
            if "could not convert string" in str(e):
                raise ValueError("El monto debe ser un valor numerico Ejm: 125")
            raise e

    def _validar_texto(self, texto: str, campo: str) -> str:
        if not isinstance(texto, str) or not texto.strip() :  #Sirve para verificar si un objeto o variable pertenece a un tipo de dato o clase en especifico.
            raise ValueError(f"El campo '{campo}' no puede estar vacio") 
        return texto.strip().capitalize()


    def _validar_tipo(self, tipo: str) -> str:
        tipo_limpio = str(tipo).strip().lower()
        if tipo_limpio not in ['ingreso', 'gasto']:
            raise ValueError("El tipo debe ser estrictamente un ingresos o gasto.")
        return tipo_limpio 

    def __str__(self):
        signo = "+" if self.tipo == 'ingreso' else "-"
        return f"[{self.fecha}] {self.concepto} ({self.categoria}): {signo}${self.monto:.2f}"
#-------------------------------------------------------------------------------------------------------

class CalculadoraFinanciera:
    def __init__(self):
        self.historial = []

    def agregar_transaccion(self,transaccion: Transaccion):
        if not isinstance(transaccion, Transaccion):
            raise TypeError("Solo se pueden agregar objetos de la clase transaccion")
        self.historial.append(transaccion)
        print(f"La transaccion fue agregada con exito: {transaccion.concepto}")

    def calcular_balance(self) -> float:
     balance = 0.0
     for t in self.historial:
        if t.tipo == 'ingreso':
            balance += t.monto
        elif t.tipo == 'gasto':
            balance -= t.monto
     return balance

    def resumen_por_categoria(self, tipo : str = 'gasto') -> dict:
     resumen = {}
     for t in self.historial:
        if t.tipo == tipo:
            resumen[t.categoria] = resumen.get(t.categoria, 0.0) + t.monto
            return resumen

    def mostrar_reporte(self):
     print("\n=== 📊 REPORTE FINANCIERO ===")
     if not self.historial:
        print("No hay transaccionas registradas")
        return

     for t in self.historial:
        print(" ", t)

     print("-" * 30)
     print(f" Balance Total: {self.calcular_balance():.2f}")

    print("-" * 30)

#-------------------------------------------------------------------------
#Conection with console, and excepts for errors.

    def registrar_desde_consola(calculadora: CalculadoraFinanciera):
     print("\n--- ✍️ REGISTRAR NUEVA TRANSACCIÓN ---")
     while True:
        try:
            monto_input = input("1. Ingrese el monto (o (s) para salir): ")
            if monto_input.lower() == 's':
                break

            concepto = input("2. Concepto (ej. Supermercado): ")
            categoria = input("3. Cateogiria (ej. Alimentacion, Salario, Ocio): ")
            tipo = input("4. Tipo (ingreso o gasto):" )

    
            nueva_transaccion = Transaccion(monto_input, concepto, categoria, tipo)

 
            calculadora.agregar_transaccion(nueva_transaccion)
            break
        except ValueError as error:
      
            print(f"\n❌ Error de validación: {error}")
            print("Por favor, intenga ingresar los datos nueva mente. \n")
        except Exception as error:
           
            print(f"\n❌ Error inesperado: {error}\n")

# DEMO.

if __name__ == "__main__":
    mi_planificador = CalculadoraFinanciera()

    salario = Transaccion(1500, "Quincena", "Salario", "ingreso")
    
    mi_planificador.agregar_transaccion(salario)

    mi_planificador.registrar_desde_consola()
    
    mi_planificador.mostrar_reporte()
