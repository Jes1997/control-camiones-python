# 🚚 Control de Camiones – Sistema de Registro

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite&logoColor=white)
![CLI](https://img.shields.io/badge/Interface-CLI-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

Sistema de control de **entrada y salida de camiones** desarrollado en **Python**, pensado como proyecto práctico para aplicar buenas prácticas, lógica de negocio y persistencia de datos usando **SQLite**.

---

## 📌 Características principales

- 🚛 Registro de **entrada de camiones**
- ⏱️ Registro de **salida** con cálculo de tiempo
- 📋 Listado completo de movimientos
- ✏️ Edición de registros ya cerrados
- ✅ Validación de datos y fechas
- 💾 Persistencia de datos con **SQLite**
- 🧩 Código modular y fácil de mantener

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **SQLite**
- Aplicación de consola (CLI)
- Programación estructurada
- Separación de responsabilidades

---

## 📂 Estructura del proyecto

```text
control-camiones-python/
│
├── main.py            # Punto de entrada del programa
├── database.py        # Conexión y configuración de la base de datos
├── repository.py      # Operaciones CRUD
├── models.py          # Modelos de datos
├── utils.py           # Validaciones y utilidades
├── camiones.db        # Base de datos SQLite
└── README.md
```

---

## ▶️ Cómo ejecutar el proyecto

1. Clona el repositorio:

```bash
git clone https://github.com/Jes1997/control-camiones-python.git
```

2. Accede al directorio:

```bash
cd control-camiones-python
```

3. Ejecuta el programa:

```bash
python main.py
```

- Requiere Python 3
- No necesita dependencias externas

🧠 Qué se practica con este proyecto

- Lógica de negocio aplicada a un caso real

- Gestión de bases de datos con SQLite

- Operaciones CRUD

- Validación de entradas del usuario

- Organización y limpieza del código

- Desarrollo de aplicaciones de consola

📸 Capturas

(Pendiente de añadir capturas de la ejecución por consola)

🚀 Posibles mejoras futuras

- Interfaz gráfica (Tkinter / PyQt)

- Versión web (Flask o Django)

- Exportación de datos a CSV o PDF

- Sistema de usuarios

- Tests automáticos

📄 Licencia

Este proyecto está bajo la licencia MIT.

👤 Autor

Jesús García Castillo
