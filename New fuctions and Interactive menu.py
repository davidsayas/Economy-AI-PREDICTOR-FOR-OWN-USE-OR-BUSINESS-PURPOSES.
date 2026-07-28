import json
import datetime
import os

class Transaccion:
    "Representa esa transaccion financiera la cual esta clasificada en ingreso o gasto"
    "junto a sus validaciones internas"

    def __init__(self,monto, concepto: str, categoria: str, tipo : str, fecha=None):
        self.monto = self._validar_monto(monto)
        self.concepto = self._validar_texto(concepto, "concepto")
        self.categoria = self._validar_texto(categoria, "categoria")
        self.tipo = self._validar_tipo(tipo)

        # Si cargamos DESDE JSON, usamos la fecha guardada, si es nueva, usamos la de hoy-

        if fecha:
            self.fecha = fecha
        else: 
            self.fecha = str(datetime.date.today())

    def _validar_monto(self,monto) -> float:
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError("El monto debe ser mayor a cero.")
            return monto_float
        except ValueError as e:
            if "could not convert string" in str(e):
                raise ValueError("El monto debe ser numero (Ej 145.40).")
            raise e

    def _validar_texto(self, texto: str, campo : str) -> str:
        if not isinstance(texto,str) or not texto.strip():
            raise ValueError(f"El campo '{campo}' no puede estar vacio.")
        return texto.strip().capitalize()

    def _validar_tipo(self, tipo: str) -> str:
        tipo_limpio = str(tipo).strip().lower()
        if tipo_limpio not in ['ingreso', 'gasto']:
            raise ValueError("El tipo debe ser ingreso o gasto")
        return tipo_limpio

    def to_dict(self):
        #Convertimos el objeto en un diccionario para poder guardarlo en el formato de texto json
        return {
            "monto": self.monto,
            "concepto": self.concepto,
            "categoria": self.categoria,
            "tipo": self.tipo,
            "fecha": self.fecha 
        }
    @classmethod
    def from_dict(cls, data):
        #Crea un objeto transaccion a partir de un diccionario cargado de un json.
        return cls(data["monto"]), data["concepto"], data["categoria"], data["tipo"], data["fecha"]

    def __str__(self):
        signo = "+" if self.tipo == "ingreso" else "-"
        return f"[{self.fecha}] {self.concepto} ({self.categoria}: {signo}${self.monto:.2f})"

#----------------------------------------------------------------------------------
class CalculadoraFinanciera:
    #"Gestiona la lista de transacciones, calculos y ahora la persisntecia en disco"
    def __init__(self, archivo_datos ="mis_finanzas.json"):
        self.historial = []
        self.archivo_datos = archivo_datos

    def agregar_transaccion(self, transaccion: Transaccion):
        self.historial.append(transaccion)
        print(f"Transaccion agregada: {transaccion.concepto}")

    def calcular_balance(self) -> float:
        balance = 0.0
        for t in self.historial:
            if t.tipo == "ingreso":
                balance += t.monto
            elif t.tipo == "gasto":
                balance -= t.monto
        return balance

    def mostrar_reporte(self):
        print("\n=== 📊 REPORTE FINANCIERO ===")
        if not self.historial:
            print("No hay transacciones registradas.")
            return

        for t in self.historial:
            print("", t)

        print("-" * 30)
        print(f"💰 Balance Total: ${self.calcular_balance():.2f}")

    def mostrar_resumen_categorias(self):
        print("\n=== 📂 RESUMEN POR CATEGORÍAS (GASTOS) ===")
        gastos = {}
        for t in self.historial:
            if t.tipo == "gasto":
                gastos[t.categoria] = gastos.get(t.categoria, 0.0) + t.monto # Si la categoria no esta creada, con esta linea de codigo se crea.

            if not gastos:
                print("No hay gastos registrados para resumir.")
                return

            for cat, total in gastos.items(): # Items, me daria todos los valores clave y valor.
                print(f"- {cat}: ${total:.2f}")

# ----- 
    def guardar_datos(self):
        #Guarda la lista de transacciones en un archivo JSON
        try:
            #Transformamos los objetos a diccionarios
            datos_exportar = [t.to_dict() for t in self.historial]
            with open(self.archivo_datos, 'w', encoding ='utf-8') as f:
                json.dump(datos_exportar, f , indent=4)
            print(f"\n💾 Datos guardados exitosamente en '{self.archivo_datos}'.")
        except Exception as e:
            print(f"\n❌ Error al guardar los datos: {e}")

    def cargar_datos(self):
        #Carga las transacciones desde un archivo json, protegiendo contra errores.
        if not os.path.exists(self.archivo_datos):
            print("\nℹ️ No se encontró historial previo. Iniciando base de datos limpia.")
            return
        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                datos_importados = json.load(f)
                #Reconstruimos los objetos transaccion desde los diccionarios
                self.historial = [Transaccion.from_dict(d) for d in datos_importados]
            print(f"\n📂 Se cargaron {len(self.historial)} transacciones del historial.")
        except json.JSONDecodeError:
            print("\n⚠️ El archivo de datos está corrupto. Se iniciará un historial vacío.")
        except Exception as e:
               print(f"\n❌ Error inesperado al cargar datos: {e}")

def registrar_desde_consola(calculadora: CalculadoraFinanciera):
    print("\n--- ✍️ REGISTRAR NUEVA TRANSACCIÓN ---")
    try:
        monto = input("1. Monto (ej. 150.50): ")
        concepto = input("2. Concepto (ej. Supermercado): ")
        categoria = input("3. Categoría (ej. Alimentación, Salario): ")
        tipo = input("4. Tipo ('ingreso' o 'gasto'): ")
        
        nueva_transaccion = Transaccion(monto, concepto, categoria, tipo)
        calculadora.agregar_transaccion(nueva_transaccion)
    except ValueError as error:
        print(f"\n❌ Error: {error} Inténtalo de nuevo.")


def menu_principal():
    """Motor del menú interactivo"""
    calc = CalculadoraFinanciera()
    calc.cargar_datos() # Intenta cargar datos al iniciar

    while True:
        print("\n" + "="*35)
        print("💼 MI PLANIFICADOR FINANCIERO")
        print("="*35)
        print("1. Agregar Transacción")
        print("2. Ver Reporte y Balance Total")
        print("3. Ver Resumen de Gastos por Categoría")
        print("4. Guardar y Salir")
        
        opcion = input("\n👉 Elige una opción (1-4): ")

        if opcion == '1':
            registrar_desde_consola(calc)
        elif opcion == '2':
            calc.mostrar_reporte()
        elif opcion == '3':
            calc.mostrar_resumen_categorias()
        elif opcion == '4':
            calc.guardar_datos()
            print("\n¡Hasta luego! Tus finanzas están seguras. 👋\n")
            break
        else:
            print("\n❌ Opción no válida. Ingresa un número del 1 al 4.")

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    menu_principal()

