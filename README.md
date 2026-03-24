# OptiTurno

Aplicación de escritorio desarrollada con **Python y PySide6** para registrar revisiones visuales y estimar la prioridad de atención de los pacientes.


## Problema que resuelve 

En una óptica no todas las revisiones tienen la misma urgencia. Algunos pacientes presentan síntomas más graves o llevan mucho tiempo sin revisión. Esta aplicación permite registrar esos casos y mostrar una prioridad aproximada.


## Descripción 

La aplicación permite registrar pacientes indicando:
- nombre
- nivel de síntomas
- meses desde la última revisión

Con esta información se calcula automáticamente una prioridad de atención.

## Funcionalidades 
- Interfaz gráfica con ***PySide6***
- Formulario con validación del nombre.
- Cálculo automático de prioridad
- Barra visual personalizada de prioridad 
- Tabla con revisiones registradas
- Tests Unitarios con **pytest**

## Ejecutar la aplicación
- Instalar dependencias:
  1. pip install PySide6 
  2. pip install pytest


- Ejecutar:
  1. python main.py

## Cómo ejecutar los tests
- pytest -v 

## Estructura del proyecto 
```
reto_3
│
├── main.py
├── README.md
│
├── app
│ ├── init.py
│ ├── main_window.py
│ ├── models.py
│ ├── validators.py
│ └── widgets.py
│
└── tests
├─
└── test_logic.py
```