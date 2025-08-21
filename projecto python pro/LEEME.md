# Proyecto de Gestión de Eventos con Python y Tkinter

## Descripción General
Este proyecto es una aplicación de escritorio desarrollada en Python que permite gestionar eventos dentro de una organización. La aplicación utiliza **Tkinter** para la interfaz gráfica y **SQLite** para el almacenamiento de datos. Los usuarios pueden crear, buscar y eliminar eventos de manera eficiente.

El proyecto incluye características dinámicas dependiendo del tipo de evento, como selección de fecha, hora, lugar y área involucrada. Además, permite la gestión de eventos a través de un menú principal intuitivo y tablas interactivas.

---

## Librerías y Dependencias
El proyecto utiliza las siguientes librerías:

- `tkinter` → Librería estándar de Python para construir interfaces gráficas.
- `tkcalendar` → Permite seleccionar fechas de manera visual (`DateEntry`).
- `sqlite3` → Librería estándar de Python para manejo de bases de datos SQLite.
- `ttk` → Extensión de Tkinter para widgets modernos como `Treeview` y `Combobox`.

> Nota: `tkinter`, `ttk` y `sqlite3` vienen con Python y no requieren instalación externa. `tkcalendar` debe instalarse vía `pip`.

Archivo de requerimientos: `requirements.txt`  

---

## Funcionalidades Principales

### 1. Login
- Captura usuario y contraseña mediante `Entry`.
- Valida credenciales usando un diccionario de usuarios predefinido.
- Mensajes de error claros si el usuario no existe o la contraseña es incorrecta.

### 2. Menú Principal
- Interfaz con botones gráficos para:
  - Agregar evento
  - Buscar eventos
  - Eliminar eventos
- Menú responsive que abre nuevas ventanas (`Toplevel`) según la opción seleccionada.

### 3. Agregar Evento
- Campos dinámicos según el tipo de evento seleccionado:
  - **Capacitación SST** → fecha, lugar y área.
  - **Inspección de seguridad** → fecha, lugar y área.
  - **Simulacro de evacuación** → fecha, hora, minutos y área.
  - **Entrega de EPP** → fecha, lugar y área.
- Validaciones para asegurar que todos los campos requeridos sean completados.
- Confirmación antes de guardar los datos en SQLite.

### 4. Buscar Evento
- Muestra todos los eventos almacenados en un `Treeview`.
- Permite filtrar por nombre de evento.
- Menú contextual (clic derecho) para eliminar eventos directamente desde la tabla.

### 5. Eliminar Evento
- Permite eliminar un evento seleccionado del `Treeview` y de la base de datos.
- Solicita confirmación antes de realizar la eliminación.
- Actualiza la tabla inmediatamente tras eliminar.

---

## Base de Datos
- Archivo: `info.db`
- Tabla: `eventos`
- Columnas:
  - `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  - `Evento` (TEXT)
  - `tipo_evento` (TEXT)
  - `Fecha` (TEXT)
  - `Hora` (TEXT)
  - `Minutos` (TEXT)
  - `Lugar` (TEXT)
  - `Area` (TEXT)

> La base de datos se crea automáticamente si no existe.

---

## Estructura del Proyecto
proyecto_eventos/
│
├─ main.py # Archivo principal con la lógica de la aplicación
├─ info.db # Base de datos SQLite
├─ requirements.txt # Librerías necesarias
├─ LEEME.md # Descripción y documentación del proyecto
└─ imagenes/ # Carpeta con iconos y recursos gráficos
├─ logo.ico
├─ Calendario.png
├─ Add.png
└─ Delete.png

---

## Ejecución Paso a Paso
1. Abre la terminal o consola.
2. Navega a la carpeta del proyecto.
3. Instala las dependencias externas:
4. Ejecuta el programa principal:
5. Ingresa usuario y contraseña para acceder al menú principal.

---

## Mejoras Futuras
- Roles de usuario con distintos permisos.
- Exportación de eventos a Excel o PDF.
- Edición de eventos existentes.
- Estadísticas gráficas por área o tipo de evento.

---

## Usuario de Prueba
- Usuario: `admin`
- Contraseña: `1234`

---

## Autor
- Nombre: Andres David mendoza