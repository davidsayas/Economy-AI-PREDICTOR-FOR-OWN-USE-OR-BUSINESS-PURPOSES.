# 💼 Planificador Financiero con Inteligencia Artificial (Python)

Un sistema de gestión de finanzas personales desarrollado en **Python** que combina Programación Orientada a Objetos (POO), persistencia de datos local en formato JSON y un modelo predictivo de **Machine Learning** (Regresión Lineal) para anticipar gastos y emitir alertas presupuestarias tempranas.

---

## ✨ Características Principales

* **Arquitectura Orientada a Objetos (POO):** Clases estructuradas (`Transaccion` y `CalculadoraFinanciera`) con validaciones internas robustas para montos, textos y tipos de transacciones.
* **Persistencia de Datos:** Guardado y carga automática de transacciones mediante archivos JSON (`mis_finanzas.json`).
* **Reportes Financieros:** Cálculo de balance en tiempo real y desglose automatizado de gastos agrupados por categorías.
* **🤖 Proyección de Gastos con Machine Learning:** Utiliza `pandas` para ingeniería de características e Inteligencia Artificial (`scikit-learn` - Regresión Lineal) para analizar el comportamiento diario del mes en curso y proyectar el gasto total al cierre del período.
* **Sistema de Alerta Temprana:** Compara la proyección matemática de fin de mes con el presupuesto límite del usuario para advertir sobre posibles déficits o felicitar por finanzas sanas.

---

## 🛠️ Tecnologías y Librerías Utilizadas

* **Python 3.x**
* **Pandas** (Manipulación y transformación de datos temporales)
* **Scikit-Learn** (Modelo de Regresión Lineal)
* **NumPy** (Operaciones numéricas)
* **Módulos nativos:** `json`, `datetime`, `calendar`, `os`

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone [https://github.com/davidsayas/Economy-AI-PREDICTOR-FOR-OWN-USE-OR-BUSINESS-PURPOSES..git](https://github.com/davidsayas/Economy-AI-PREDICTOR-FOR-OWN-USE-OR-BUSINESS-PURPOSES..git)
cd Economy-AI-PREDICTOR-FOR-OWN-USE-OR-BUSINESS-PURPOSES.

## 📄 Licencia

Distribuido bajo la Licencia **MIT**. Consulta el archivo `LICENSE` para más información.

<div align="center">
  <sub>Hecho con 💜 por <a href="https://github.com">Tu Nombre</a></sub>
</div>
