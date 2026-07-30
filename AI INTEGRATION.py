import json
import datetime
import calendar
import os

# --- LIBRERÍAS DE MACHINE LEARNING ---
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class Transaccion:
    """
    Representa una transacción financiera individual (ingreso o gasto).
    Incluye validación interna.
    """
    def __init__(self, monto, concepto: str, categoria: str, tipo: str, fecha=None):
        self.monto = self._validar_monto(monto)
        self.concepto = self._validar_texto(concepto, "concepto")
        self.categoria = self._validar_texto(categoria, "categoría")
        self.tipo = self._validar_tipo(tipo)
        # Si cargamos desde JSON, usamos la fecha guardada. Si es nueva, usamos la de hoy.
        if fecha:
            self.fecha = fecha
        else:
            self.fecha = str(datetime.date.today())

    def _validar_monto(self, monto) -> float:
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError("El monto debe ser mayor a cero.")
            return monto_float
        except ValueError as e:
            if "could not convert string" in str(e):
                raise ValueError("El monto debe ser numérico (ej. 150.50).")
            raise e

    def _validar_texto(self, texto: str, campo: str) -> str:
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        return texto.strip().capitalize()

    def _validar_tipo(self, tipo: str) -> str:
        tipo_limpio = str(tipo).strip().lower()
        if tipo_limpio not in ['ingreso', 'gasto']:
            raise ValueError("El tipo debe ser 'ingreso' o 'gasto'.")
        return tipo_limpio

    def to_dict(self):
        """Convierte el objeto en un diccionario para poder guardarlo en JSON."""
        return {
            "monto": self.monto,
            "concepto": self.concepto,
            "categoria": self.categoria,
            "tipo": self.tipo,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Transaccion a partir de un diccionario cargado de un JSON."""
        return cls(data["monto"], data["concepto"], data["categoria"], data["tipo"], data["fecha"])

    def __str__(self):
        signo = "+" if self.tipo == 'ingreso' else "-"
        return f"[{self.fecha}] {self.concepto} ({self.categoria}): {signo}${self.monto:.2f}"


class CalculadoraFinanciera:
    """
    Gestiona la lista de transacciones, persistencia y ahora Machine Learning predictivo.
    """
    def __init__(self, archivo_datos="mis_finanzas.json"):
        self.historial = []
        self.archivo_datos = archivo_datos

    def agregar_transaccion(self, transaccion: Transaccion):
        self.historial.append(transaccion)
        print(f"✔ Transacción agregada: {transaccion.concepto}")

    def calcular_balance(self) -> float:
        balance = 0.0
        for t in self.historial:
            if t.tipo == 'ingreso':
                balance += t.monto
            elif t.tipo == 'gasto':
                balance -= t.monto
        return balance

    def mostrar_reporte(self):
        print("\n=== 📊 REPORTE FINANCIERO ===")
        if not self.historial:
            print("No hay transacciones registradas.")
            return
        
        for t in self.historial:
            print(" ", t)
            
        print("-" * 30)
        print(f"💰 Balance Total: ${self.calcular_balance():.2f}")

    def mostrar_resumen_categorias(self):
        print("\n=== 📂 RESUMEN POR CATEGORÍAS (GASTOS) ===")
        gastos = {}
        for t in self.historial:
            if t.tipo == 'gasto':
                gastos[t.categoria] = gastos.get(t.categoria, 0.0) + t.monto
        
        if not gastos:
            print("No hay gastos registrados para resumir.")
            return
            
        for cat, total in gastos.items():
            print(f" - {cat}: ${total:.2f}")

    def guardar_datos(self):
        try:
            datos_exportar = [t.to_dict() for t in self.historial]
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos_exportar, f, indent=4)
            print(f"\n💾 Datos guardados exitosamente.")
        except Exception as e:
            print(f"\n❌ Error al guardar: {e}")

    def cargar_datos(self):
        if not os.path.exists(self.archivo_datos):
            return
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                datos_importados = json.load(f)
                self.historial = [Transaccion.from_dict(d) for d in datos_importados]
        except json.JSONDecodeError:
            print("\n⚠️ Archivo de datos corrupto. Iniciando vacío.")

    # --- NUEVO MÉTODO DEL SPRINT 3: MACHINE LEARNING ---
    def proyectar_gastos_ia(self, presupuesto=None):
        print("\n=== 🤖 PREDICCIÓN DE GASTOS CON INTELIGENCIA ARTIFICIAL ===")
        print("🔍 [DEBUG] Iniciando análisis...")
        
        # 1. Extraer solo los gastos
        gastos = [t for t in self.historial if t.tipo == 'gasto']
        print(f"🔍 [DEBUG] Se encontraron {len(gastos)} gastos en total en el historial.")
        
        if not gastos:
            print("❌ Necesitas registrar gastos para entrenar a la IA.")
            return

        # 2. Transformar los datos para el análisis usando pandas
        df = pd.DataFrame([t.to_dict() for t in gastos])
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Filtrar solo el mes actual
        hoy = datetime.date.today()
        print(f"🔍 [DEBUG] Filtrando gastos para el mes {hoy.month} del año {hoy.year}...")
        
        df = df[(df['fecha'].dt.year == hoy.year) & (df['fecha'].dt.month == hoy.month)]
        print(f"🔍 [DEBUG] Gastos válidos encontrados para este mes: {len(df)}")
        
        if df.empty:
            print("❌ No hay gastos en el mes actual para hacer proyecciones.")
            return

        # 3. Ingeniería de Características (Feature Engineering)
        df['dia_del_mes'] = df['fecha'].dt.day
        gastos_diarios = df.groupby('dia_del_mes')['monto'].sum().reset_index()
        gastos_diarios = gastos_diarios.sort_values(by='dia_del_mes')
        gastos_diarios['gasto_acumulado'] = gastos_diarios['monto'].cumsum()
        print(f"🔍 [DEBUG] Días distintos con gastos registrados este mes: {len(gastos_diarios)}")

        # Validación algorítmica: Una recta necesita al menos 2 puntos
        if len(gastos_diarios) < 2:
            print("⚠️ IA no disponible: Registra gastos en al menos 2 días distintos del mes para detectar un patrón.")
            print(f"Gasto actual: ${gastos_diarios['gasto_acumulado'].max():.2f}")
            return

        # 4. Entrenamiento del Modelo de Regresión Lineal
        print("🔍 [DEBUG] Entrenando modelo matemático con scikit-learn...")
        X = gastos_diarios[['dia_del_mes']]
        y = gastos_diarios['gasto_acumulado']

        modelo = LinearRegression()
        modelo.fit(X, y)

        # 5. Predicción
        _, dias_del_mes = calendar.monthrange(hoy.year, hoy.month)
        X_futuro = pd.DataFrame({'dia_del_mes': [dias_del_mes]})
        prediccion_fin_mes = modelo.predict(X_futuro)[0]
        
        gasto_actual = gastos_diarios['gasto_acumulado'].max()

        # 6. Reporte Inteligente
        print(f"\n📈 Modelo entrenado con actividad de {len(gastos_diarios)} días.")
        print(f"💵 Gasto acumulado a hoy (Día {hoy.day}): ${gasto_actual:.2f}")
        print(f"🔮 Proyección matemática para fin de mes (Día {dias_del_mes}): ${prediccion_fin_mes:.2f}")
        
        # 7. Sistema de Alerta Temprana
        if presupuesto:
            print("-" * 30)
            if prediccion_fin_mes > presupuesto:
                deficit = prediccion_fin_mes - presupuesto
                print(f"🚨 ALERTA ROJA: Al ritmo actual, superarás tu presupuesto por ${deficit:.2f}.")
                print("💡 Sugerencia: Reduce tus gastos no esenciales en los próximos días.")
            else:
                sobrante = presupuesto - prediccion_fin_mes
                print(f"✅ FINANZAS SANAS: Al ritmo actual, terminarás el mes respetando tu presupuesto.")
                print(f"🎉 Te podrían sobrar aprox. ${sobrante:.2f}.")

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
    calc = CalculadoraFinanciera()
    calc.cargar_datos() 

    while True:
        print("\n" + "="*45)
        print("💼 PLANIFICADOR FINANCIERO CON IA")
        print("="*45)
        print("1. Agregar Transacción")
        print("2. Ver Reporte y Balance Total")
        print("3. Ver Resumen de Gastos por Categoría")
        print("4. 🤖 Predecir Gastos a Fin de Mes (IA)")
        print("5. Guardar y Salir")
        
        opcion = input("\n👉 Elige una opción (1-5): ")

        if opcion == '1':
            registrar_desde_consola(calc)
        elif opcion == '2':
            calc.mostrar_reporte()
        elif opcion == '3':
            calc.mostrar_resumen_categorias()
        elif opcion == '4':
            try:
                presupuesto_str = input("¿Cuál es tu límite máximo de gastos para este mes? ($): ")
                presupuesto_float = float(presupuesto_str)
                calc.proyectar_gastos_ia(presupuesto=presupuesto_float)
            except ValueError:
                print("❌ Error: Ingresa un número válido para el presupuesto.")
                
        elif opcion == '5':
            calc.guardar_datos()
            print("\n¡Hasta luego! Tus finanzas están seguras. 👋\n")
            break
        else:
            print("\n❌ Opción no válida. Ingresa un número del 1 al 5.")


if __name__ == "__main__":
    menu_principal()