import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

# Crear o conectar a la base de datos
conexion = sqlite3.connect("info.db") # (Evento, tipo evento, Fecha, Hora, Minutos, Lugar, Area)
cursor = conexion.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Evento TEXT NOT NULL,
    tipo_evento TEXT NOT NULL,
    Fecha TEXT NOT NULL,
    Hora TEXT,
    Minutos TEXT,
    lugar TEXT,
    Area TEXT
)
""")
conexion.commit()


widgets_dinamicos = []

usuarios = {"admin":"1234"} #diccionario de usuarios creados
areas = ["Administración","Operaciones / Producción","Mantenimiento","Almacén / Logística","Seguridad Industrial","Recursos Humanos","Transporte","Todos los departamentos"]
columnas = ("ID","Evento","Tipo evento","Fecha","Hora","Lugar","Area")

def login(): #funcion para validar usuario y contrasena
    user = entrada_usuario.get() # captura de usuario
    password = entrada_contra.get() # captura de contrasena
    if (user in usuarios) and (password == usuarios[user]):
        crear_menu()
    elif user not in usuarios:
        messagebox.showerror("Error", "El usuario no existe")
    else:
        messagebox.showerror("Error", "Contraseña incorrecta intente de nuevo")
    
def crear_inicio():# funcion para crear la parte grafica del login
    global entrada_usuario
    global entrada_contra
    global inicio

    inicio = tk.Tk()
    inicio.title("Login")
    inicio.iconbitmap("imagenes\logo.ico")#cambiar logo de la pantalla
    inicio.geometry("600x300")
    inicio.configure(bg="#90b2e2") 
    inicio.resizable(False, False)

    texto1 = tk.Label(inicio,text="Login",font=("times new roman",19),bg="#90b2e2")
    texto1.place(relx=0.5,rely=0.1,anchor="center")

    texto2 = tk.Label(inicio,text="Ingrese el usuario",font=("times new roman",12),bg="#90b2e2")
    texto2.place(relx=0.25,rely=0.3,anchor="center")

    entrada_usuario = tk.Entry(inicio, font=("times new roman", 12))
    entrada_usuario.place(relx=0.52,rely=0.3,anchor="center")

    texto3 = tk.Label(inicio,text="Ingrese la contraseña",font=("times new roman",12),bg="#90b2e2")
    texto3.place(relx=0.23,rely=0.5,anchor="center")

    entrada_contra = tk.Entry(inicio, font=("times new roman", 12), show='*')
    entrada_contra.place(relx=0.52,rely=0.5,anchor="center")

    Inicio = tk.Button(inicio, text="Iniciar sesión",command=login,font=("times new roman",12),bg="#85d489")
    Inicio.place(relx=0.5, rely=0.7, anchor="center")

    inicio.mainloop()

def crear_menu(): #funcion para el menu principal

    global Ruta_calendario , Ruta_agregar, Ruta_eliminar, menu


    inicio.withdraw()
    menu = tk.Toplevel()
    menu.title("Menu principal")
    menu.iconbitmap("imagenes\logo.ico")#cambiar logo de la pantalla
    menu.geometry("900x200")
    menu.resizable(False, False)
    menu.configure(bg="#90b2e2") 
    menu.protocol("WM_DELETE_WINDOW",cerrar)

    #rutas imagenes
    Ruta_calendario = tk.PhotoImage(file="imagenes\Calendario.png") 
    Ruta_agregar = tk.PhotoImage(file="imagenes\Add.png")
    Ruta_eliminar = tk.PhotoImage(file="imagenes\Delete.png")

    boton_calendario = tk.Button(menu,text="Buscar eventos" ,compound="top",font=("times new roman",19), image=Ruta_calendario ,bd=0, command=buscar_eventos,bg="#90b2e2")
    boton_calendario.place(relx=0.5, rely=0.6, anchor="center")

    boton_agregar = tk.Button(menu,text="Agregar evento" ,compound="top",font=("times new roman",19), image=Ruta_agregar,bd=0, command=Agregar_evento,bg="#90b2e2")
    boton_agregar.place(relx=0.2, rely=0.6, anchor="center")

    boton_eliminar = tk.Button(menu, text="Eliminar evento" ,compound="top",font=("times new roman",19), image=Ruta_eliminar,bd=0, command=eliminar_eventos,bg="#90b2e2")
    boton_eliminar.place(relx=0.8, rely=0.6, anchor="center")

    texto1 = tk.Label(menu,text="Seleciona la operación a realizar",font=("times new roman",19),bg="#90b2e2")
    texto1.place(relx=0.5,rely=0.1,anchor="center")

def buscar_eventos():
    global eventos, tabla

    menu.withdraw()
    eventos = tk.Toplevel()
    eventos.title("Agregar un nuevo evento")
    eventos.iconbitmap("imagenes\icono_bd.ico")#cambiar logo de la pantalla
    eventos.geometry("1500x300")
    eventos.resizable(False, False)
    eventos.configure(bg="#90b2e2") 
    eventos.protocol("WM_DELETE_WINDOW",cerrar)

    conn = sqlite3.connect("info.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, Evento, tipo_evento, Fecha, Hora, Minutos, lugar, Area FROM eventos")

    tabla = ttk.Treeview(eventos, columns=columnas, show= "headings")
    tabla.pack(fill="both", expand=True)

    anchos = (60, 240, 180, 110, 70, 80, 260, 180)
    for col, ancho in zip(columnas, anchos):
        tabla.heading(col, text=col)
        tabla.column(col, width=ancho, anchor="center")


    for evento in cursor.fetchall():
        tabla.insert("", tk.END, values=evento)

    conn.close()

    # Menú click derecho
    menu_contextual = tk.Menu(eventos, tearoff=0)
    menu_contextual.add_command(label="Eliminar evento", command=eliminar)
    
    # Mostrar menú contextual con clic derecho
    def mostrar_menu(event):
        seleccionado = tabla.identify_row(event.y)
        if seleccionado:
            tabla.selection_set(seleccionado)  # Selecciona la fila donde hiciste clic
            menu_contextual.post(event.x_root, event.y_root)

    tabla.bind("<Button-3>", mostrar_menu)# captura click derecho sobre la tabla

    boton_volver = tk.Button(eventos,text="Volver al menu" ,compound="top",font=("times new roman",10), bd=0, command=volver_menu,bg="#e64529")
    boton_volver.place(relx=0.97,rely=0.05, anchor="center")

def eliminar_eventos():
    global eliminar_evento, tabla

    menu.withdraw()
    eliminar_evento = tk.Toplevel()
    eliminar_evento.title("Agregar un nuevo evento")
    eliminar_evento.iconbitmap("imagenes\icono_delete.ico")#cambiar logo de la pantalla
    eliminar_evento.geometry("900x300")
    eliminar_evento.resizable(False, False)
    eliminar_evento.configure(bg="#90b2e2") 
    eliminar_evento.protocol("WM_DELETE_WINDOW",cerrar)    

    texto1 = tk.Label(eliminar_evento, text="Agrega la información del evento a eliminar",font=("times new roman",19),bg="#90b2e2")
    texto1.place(relx=0.5,rely=0.1,anchor="center")

    texto2 = tk.Label(eliminar_evento,text="Ingrese el nombre del evento",font=("times new roman",14),bg="#90b2e2")
    texto2.place(relx=0.15,rely=0.3,anchor="center")

    entrada_nombre_evento = tk.Entry(eliminar_evento, font=("times new roman", 12),width=50,bd=0)
    entrada_nombre_evento.place(relx=0.5,rely=0.3,anchor="center")

    
    def buscar_evento():
        # Simulación: aquí buscarías el evento en tu base de datos o lista
        nombre_buscado = entrada_nombre_evento.get()

        # Limpia resultados previos
        for fila in tabla.get_children():
            tabla.delete(fila)
        try:
            conn = sqlite3.connect("info.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, Evento, tipo_evento, Fecha, Hora, Minutos, lugar, Area
                FROM eventos
                WHERE Evento LIKE ?
            """, ('%' + nombre_buscado + '%',))

            resultados = cursor.fetchall()
            conn.close()

            # Mostrar resultados en la tabla
            for evento in resultados:
                tabla.insert("", "end", values=evento)

        except Exception as e:
            print("Error al buscar:", e)

    # Frame para la tabla de resultados
    frame_tabla = tk.Frame(eliminar_evento, bg="#90b2e2")
    frame_tabla.place(relx=0.5, rely=0.65, anchor="center", width=800, height=120)

    # Treeview para mostrar resultados
    columnas = ("id","nombre","tipo","fecha")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=4)

    tabla.heading("id", text="Id")
    tabla.heading("nombre", text="Nombre del Evento")
    tabla.heading("fecha", text="Fecha")
    tabla.heading("tipo", text="Tipo de evento")

    tabla.pack(fill="both", expand=True)

    # Botón para eliminar seleccionado
    boton_eliminar = tk.Button(eliminar_evento, text="Eliminar seleccionado", font=("times new roman", 12),
                                bg="#d9534f", fg="white", command=eliminar)
    boton_eliminar.place(relx=0.5, rely=0.9, anchor="center")

    # Botón para buscar el evento
    boton_buscar = tk.Button(eliminar_evento, text="Buscar", font=("times new roman", 12),
                              command=buscar_evento, bg="#f0ad4e")
    boton_buscar.place(relx=0.8, rely=0.3, anchor="center")


    boton_volver = tk.Button(eliminar_evento,text="Volver al menu" ,compound="top",font=("times new roman",10), bd=0, command=volver_menu,bg="#e64529")
    boton_volver.place(relx=0.95,rely=0.05, anchor="center")




def Agregar_evento():
    global nuevo_evento, opciones, entrada_nombre_evento,Selecion_tipo_evento

    menu.withdraw()
    nuevo_evento = tk.Toplevel()
    nuevo_evento.title("Agregar un nuevo evento")
    nuevo_evento.iconbitmap("imagenes\icono_add.ico")#cambiar logo de la pantalla
    nuevo_evento.geometry("900x300")
    nuevo_evento.resizable(False, False)
    nuevo_evento.configure(bg="#90b2e2") 
    nuevo_evento.protocol("WM_DELETE_WINDOW",cerrar)

    opciones = ["Capacitación SST", "Inspección de seguridad", "Simulacro de evacuación", "Entrega de EPP"]


    texto1 = tk.Label(nuevo_evento, text="Agrega la información del evento",font=("times new roman",19),bg="#90b2e2")
    texto1.place(relx=0.5,rely=0.1,anchor="center")

    texto2 = tk.Label(nuevo_evento,text="Ingrese el nombre del evento",font=("times new roman",14),bg="#90b2e2")
    texto2.place(relx=0.15,rely=0.3,anchor="center")

    entrada_nombre_evento = tk.Entry(nuevo_evento, font=("times new roman", 12),width=50,bd=0)
    entrada_nombre_evento.place(relx=0.5,rely=0.3,anchor="center")

    texto3 = tk.Label(nuevo_evento,text="Seleciona el tipo de actividad",font=("times new roman",14),bg="#90b2e2")
    texto3.place(relx=0.15,rely=0.42,anchor="center")

    Selecion_tipo_evento = ttk.Combobox(nuevo_evento, values=opciones, font=("times new roman", 12),width=30)
    Selecion_tipo_evento.set("Seleccione un tipo de evento")
    Selecion_tipo_evento.place(relx=0.422,rely=0.42,anchor="center")
    Selecion_tipo_evento.bind("<<ComboboxSelected>>", verificar_tipo)

    boton_guardar = tk.Button(nuevo_evento,text="Guardar evento" ,compound="top",font=("times new roman",19), bd=0, command=Guardar_evento,bg="#85d489")
    boton_guardar.place(relx=0.5,rely=0.9, anchor="center")

    boton_volver = tk.Button(nuevo_evento,text="Volver al menu" ,compound="top",font=("times new roman",10), bd=0, command=volver_menu,bg="#e64529")
    boton_volver.place(relx=0.95,rely=0.05, anchor="center")

def verificar_tipo(event):
    global widgets_dinamicos, areas, entrada_fecha_nuevo_evento,entrada_lugar_nuevo_evento,Selecion_area,entrada_hora_nuevo_evento,entrada_minutos_nuevo_evento
    Tipo_evento = event.widget.get()
    nuevo_evento.configure(bg="#90b2e2") 

    for w in widgets_dinamicos:
        w.destroy()
    widgets_dinamicos = []  # reseteamos la lista

    if Tipo_evento == "Capacitación SST":
        
        texto4 = tk.Label(nuevo_evento, text="Escribe la fecha de la capacitación",font=("times new roman",14),bg="#90b2e2")
        texto4.place(x=25,y=150,anchor="nw")
        
        entrada_fecha_nuevo_evento = DateEntry(nuevo_evento, date_pattern="dd/mm/yyyy", font=("times new roman", 12))
        entrada_fecha_nuevo_evento.place(x=300,y=150,anchor="nw")

        texto5 = tk.Label(nuevo_evento, text="Escribe el lugar de la capacitación",font=("times new roman",14),bg="#90b2e2")
        texto5.place(x=25,y=180,anchor="nw")

        entrada_lugar_nuevo_evento = tk.Entry(nuevo_evento, font=("times new roman", 12),width=50,bd=0)
        entrada_lugar_nuevo_evento.place(x=300,y=180,anchor="nw")

        texto6 = tk.Label(nuevo_evento, text="Escribe el area de la capacitación",font=("times new roman",14),bg="#90b2e2")
        texto6.place(x=25,y=210,anchor="nw")

        Selecion_area = ttk.Combobox(nuevo_evento, values=areas, font=("times new roman", 12),width=30)
        Selecion_area.set("Seleccione el área a capacitar")
        Selecion_area.place(x=300,y=210,anchor="nw")



    elif Tipo_evento == "Inspección de seguridad":

        texto4 = tk.Label(nuevo_evento, text="Escribe la fecha de la Inspección",font=("times new roman",14),bg="#90b2e2")
        texto4.place(x=25,y=150,anchor="nw")

        entrada_fecha_nuevo_evento = DateEntry(nuevo_evento, date_pattern="dd/mm/yyyy", font=("times new roman", 12))
        entrada_fecha_nuevo_evento.place(x=280,y=150,anchor="nw")

        texto5 = tk.Label(nuevo_evento, text="Escribe el lugar de la Inspección",font=("times new roman",14),bg="#90b2e2")
        texto5.place(x=25,y=180,anchor="nw")

        entrada_lugar_nuevo_evento = tk.Entry(nuevo_evento, font=("times new roman", 12),width=50,bd=0)
        entrada_lugar_nuevo_evento.place(x=280,y=180,anchor="nw")

        texto6 = tk.Label(nuevo_evento, text="Escribe el area de la Inspección",font=("times new roman",14),bg="#90b2e2")
        texto6.place(x=25,y=210,anchor="nw")

        Selecion_area = ttk.Combobox(nuevo_evento, values=areas, font=("times new roman", 12),width=30)
        Selecion_area.set("Seleccione el área a Inspecionar")
        Selecion_area.place(x=280,y=210,anchor="nw")

    elif Tipo_evento == "Simulacro de evacuación":

        texto4 = tk.Label(nuevo_evento, text="Escribe la fecha del simulacro",font=("times new roman",14),bg="#90b2e2")
        texto4.place(x=25,y=150,anchor="nw")

        entrada_fecha_nuevo_evento = DateEntry(nuevo_evento, date_pattern="dd/mm/yyyy", font=("times new roman", 12))
        entrada_fecha_nuevo_evento.place(x=260,y=150,anchor="nw")

        texto5 = tk.Label(nuevo_evento, text="Escribe la hora del simulacro",font=("times new roman",14),bg="#90b2e2")
        texto5.place(x=25,y=180,anchor="nw")

        entrada_hora_nuevo_evento = tk.Spinbox(nuevo_evento, from_=0, to=23, width=3, format="%02.0f")
        entrada_hora_nuevo_evento.place(x=260,y=180,anchor="nw")

        entrada_minutos_nuevo_evento = tk.Spinbox(nuevo_evento, from_=0, to=59, width=3, format="%02.0f")
        entrada_minutos_nuevo_evento.place(x=290,y=180,anchor="nw")

        texto6 = tk.Label(nuevo_evento, text="Escribe el area del simulacro",font=("times new roman",14),bg="#90b2e2")
        texto6.place(x=25,y=210,anchor="nw")

        Selecion_area = ttk.Combobox(nuevo_evento, values=areas, font=("times new roman", 12),width=30)
        Selecion_area.set("Seleccione el área del simulacro")
        Selecion_area.place(x=260,y=210,anchor="nw")

    elif Tipo_evento == "Entrega de EPP":

        texto4 = tk.Label(nuevo_evento, text="Escribe la fecha de Entrega de EPP",font=("times new roman",14),bg="#90b2e2")
        texto4.place(x=25,y=150,anchor="nw")

        entrada_fecha_nuevo_evento = DateEntry(nuevo_evento, date_pattern="dd/mm/yyyy", font=("times new roman", 12))
        entrada_fecha_nuevo_evento.place(x=300,y=150,anchor="nw")

        texto5 = tk.Label(nuevo_evento, text="Escribe el lugar de Entrega de EPP",font=("times new roman",14),bg="#90b2e2")
        texto5.place(x=25,y=180,anchor="nw")

        entrada_lugar_nuevo_evento = tk.Entry(nuevo_evento, font=("times new roman", 12),width=50,bd=0)
        entrada_lugar_nuevo_evento.place(x=300,y=180,anchor="nw")

        texto6 = tk.Label(nuevo_evento, text="Escribe el area de Entrega de EPP",font=("times new roman",14),bg="#90b2e2")
        texto6.place(x=25,y=210,anchor="nw")

        Selecion_area = ttk.Combobox(nuevo_evento, values=areas, font=("times new roman", 12),width=30)
        Selecion_area.set("Seleccione el área para entregar EPP")
        Selecion_area.place(x=300,y=210,anchor="nw")

    widgets_dinamicos.append(texto4)
    widgets_dinamicos.append(texto5)
    widgets_dinamicos.append(texto6)
    widgets_dinamicos.append(entrada_fecha_nuevo_evento)
    try:
        widgets_dinamicos.append(entrada_lugar_nuevo_evento)
    except:
        pass
    widgets_dinamicos.append(Selecion_area)
    try:
        widgets_dinamicos.append(entrada_hora_nuevo_evento)
        widgets_dinamicos.append(entrada_minutos_nuevo_evento)
    except:
        pass 

def volver_menu():
    try:
        nuevo_evento.destroy()
    except:
        pass
    try:
        eliminar_evento.destroy()
    except:
        pass
    try:
        eventos.destroy()
    except:
        pass
    menu.deiconify()

def Guardar_evento():
    global entrada_nombre_evento, Selecion_tipo_evento,entrada_fecha_nuevo_evento,entrada_lugar_nuevo_evento,Selecion_area,entrada_hora_nuevo_evento,entrada_minutos_nuevo_evento

    nombre_evento = entrada_nombre_evento.get() 
    tipo_evento = Selecion_tipo_evento.get() 
    fecha_evento = entrada_fecha_nuevo_evento.get()
    area_evento = Selecion_area.get()
    hora_evento = "NAA"
    minutos_evento = "NAA"
    lugar_evento="Planta es un simulacro"

    if tipo_evento == "Simulacro de evacuación":
        hora_evento = entrada_hora_nuevo_evento.get()
        minutos_evento = entrada_minutos_nuevo_evento.get()
    else:
        lugar_evento = entrada_lugar_nuevo_evento.get()

    if nombre_evento == "": 
        messagebox.showerror("Error", "Debes introducir un nombre para el evento")
    elif tipo_evento == "Seleccione un tipo de evento":
        messagebox.showerror("Error", "Debes Seleccione un tipo de evento")
    elif lugar_evento == "":
        messagebox.showerror("Error", "Debes introducir un lugar para el evento")
    elif area_evento == "Seleccione el área a capacitar" or area_evento == "Escribe el area de la Inspección" or area_evento == "Seleccione el área del simulacro" or area_evento == "Seleccione el área para entregar EPP":
        messagebox.showerror("Error", "Debes Seleccione el área")
    else:
        confirmar = messagebox.askyesno("Confirmar guardar", f"¿esta seguro de guardar el evento con nombre'{nombre_evento}'?")
        if confirmar:
            conexion = sqlite3.connect("info.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO eventos (Evento, tipo_evento, Fecha, Hora, Minutos, Lugar, Area) VALUES (?, ?, ?, ?, ?, ?,?)",
                        (nombre_evento, tipo_evento, fecha_evento,hora_evento,minutos_evento, lugar_evento, area_evento))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("confirmacion", "Evento guardado con exito")

def eliminar():
        global tabla
        seleccionado = tabla.selection()
        
        valores = tabla.item(seleccionado[0], "values")
        id_evento = valores[1]

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar el evento con nombre {id_evento}?")
        if confirmar:
            conn = sqlite3.connect("info.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM eventos WHERE id=?", (id_evento,))
            conn.commit()
            conn.close()

            tabla.delete(seleccionado[0])  # Eliminar de la vista
            messagebox.showinfo("Éxito", "Evento eliminado correctamente")

def cerrar():# funcion para cerrar las pantallas
    try:
        inicio.destroy()
    except:
        pass
    try:
        menu.destroy()
    except:
        pass

crear_inicio()