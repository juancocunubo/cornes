# 🐾 PuRRgramacion - Python Visual de Bloques

Entorno de desarrollo visual interactivo basado en bloques con sentencias directas de Python, diseñado para facilitar el aprendizaje y prototipado rápido de programación en Python.

![PuRRgramacion](https://raw.githubusercontent.com/juancocunubo/cornes/main/preview.png)

## 🚀 Características Principales

- **Bloques Visuales con Código Python Real**: Los bloques contienen sentencias nativas de Python (`def`, `if`, `for`, `while`, `print`, `input`, asignaciones, etc.), editables y personalizables.
- **Paleta de Bloques Categorizada**:
  - **CONTROL**: Estructuras condicionales y de repetición (`if`, `else`, `elif`, `for`, `while`).
  - **DEFINICIONES**: Funciones (`def`), clases (`class`), `return`, `yield`.
  - **VARIABLES Y TIPOS**: Asignación y tipos básicos (`int`, `str`, `float`, `bool`, `list`, `dict`, `tuple`).
  - **OPERADORES**: Operadores aritméticos, de comparación y lógicos (`+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `and`, `or`, `not`).
  - **FUNCIONES**: Funciones integradas (`print()`, `input()`, `len()`, `abs()`, `range()`).
  - **IMPORTACIONES**: `import` y `from ... import ...`.
  - **DATOS**: Literales rápidos (`'hello'`, `10`, `3.14`, `True`, `None`, listas).
- **Workspace con Cuadrícula**: Lienzo visual organizado con fondo cuadriculado, bloques estilizados en tonos pizarra oscuro y resaltado de sintaxis.
- **Panel de Variables y Objetos**: Detección dinámica mediante AST de variables y funciones activas en el script, con capacidad de agregar nuevas variables interactivamente.
- **Consola / Salida Interactiva**: Ejecución en tiempo real con Python, soporte de entradas (`input()`) y visualización limpia de resultados y errores.
- **Barra de Herramientas y Menú**: Botones para Nuevo, Abrir, Guardar, 🐾 Ejecutar (`Run`), Depurar, Ver Código Python generado y Exportar a `.py`.

## 📁 Estructura del Proyecto

```
.
├── main.py          # Punto de entrada principal
├── app.py           # Controlador central (VisualBlockEditor) y ejecución de código
├── blocks.py        # Definición de bloques, librería categorizada y bloques demo
├── generator.py     # Generador de código Python, validador AST y analizador
├── ui.py            # Interfaz gráfica moderna con DearPyGui
├── run.bat          # Lanzador rápido para Windows
├── requirements.txt # Dependencias del proyecto
└── .gitignore       # Archivos y carpetas ignorados por Git
```

## 🛠️ Instalación y Requisitos

### Requisitos:
- Python 3.9+ (Recomendado 3.11 o 3.13)
- Windows, macOS o Linux

### Instalación:
1. Clona el repositorio si aún no lo tienes:
   ```bash
   git clone https://github.com/juancocunubo/cornes.git
   cd cornes
   ```

2. (Opcional pero recomendado) Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   # En Windows:
   .venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Ejecución

Puedes iniciar la aplicación ejecutando:
```bash
python main.py
```
O en Windows haciendo doble clic en `run.bat`.
