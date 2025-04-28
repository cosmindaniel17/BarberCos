import tkinter as tk
from tkinter import ttk, messagebox
import calendar
import json
import os

# Configuración inicial
AÑO = 2025
ARCHIVO_RESERVAS = "reservas.json"
reservas = {}

# Cargar reservas desde archivo
def cargar_reservas():
    global reservas
    if os.path.exists(ARCHIVO_RESERVAS):
        with open(ARCHIVO_RESERVAS, "r") as archivo:
            reservas = json.load(archivo)
    else:
        reservas = {}

# Guardar reservas en archivo
def guardar_reservas():
    with open(ARCHIVO_RESERVAS, "w") as archivo:
        json.dump(reservas, archivo, indent=4)

# Obtener días disponibles
def obtener_dias_disponibles(mes):
    _, dias_en_mes = calendar.monthrange(AÑO, mes)
    return [dia for dia in range(1, dias_en_mes + 1) if f"{AÑO}-{mes:02d}-{dia:02d}" not in reservas or len(reservas[f"{AÑO}-{mes:02d}-{dia:02d}"]) < 16]

# Obtener horas disponibles
def obtener_horas_disponibles(fecha):
    horario = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30"]
    return [hora for hora in horario if fecha not in reservas or hora not in reservas[fecha]]

# Actualizar días disponibles
def actualizar_dias(*args):
    mes = meses[mes_var.get()]
    dias_disponibles = obtener_dias_disponibles(mes)
    dia_menu["menu"].delete(0, "end")
    for dia in dias_disponibles:
        dia_menu["menu"].add_command(label=dia, command=tk._setit(dia_var, dia))
    dia_var.set(dias_disponibles[0] if dias_disponibles else "")
    actualizar_horas()

# Actualizar horas disponibles
def actualizar_horas(*args):
    mes = meses[mes_var.get()]
    dia = dia_var.get()
    if dia:
        fecha = f"{AÑO}-{mes:02d}-{int(dia):02d}"
        horas_disponibles = obtener_horas_disponibles(fecha)
        hora_menu["menu"].delete(0, "end")
        for hora in horas_disponibles:
            hora_menu["menu"].add_command(label=hora, command=tk._setit(hora_var, hora))
        hora_var.set(horas_disponibles[0] if horas_disponibles else "")

# Reservar cita
def reservar_cita():
    mes = meses[mes_var.get()]
    dia = dia_var.get()
    hora = hora_var.get()
    
    if not dia or not hora:
        messagebox.showerror("Error", "Selecciona un mes, día y una hora")
        return
    
    fecha = f"{AÑO}-{mes:02d}-{int(dia):02d}"

    # Agregar la reserva
    if fecha not in reservas:
        reservas[fecha] = []
    reservas[fecha].append(hora)
    reservas[fecha].sort()

    # Guardar reservas en el archivo
    guardar_reservas()

    # Mostrar mensaje de éxito
    messagebox.showinfo("Éxito", f"¡Cita reservada para el {fecha} a las {hora}!")

    # ACTUALIZAR HORAS DISPONIBLES
    actualizar_horas()

# Cambiar a la pantalla de reservas
def ir_a_reservas():
    bienvenida.pack_forget()
    pantalla_reservas.pack()
    actualizar_dias()
    actualizar_horas()

# Crear interfaz
cargar_reservas()
root = tk.Tk()
root.title("BarberCos - Reserva de Citas")
root.geometry("450x350")
root.configure(bg="#222831")

# Pantalla de bienvenida
bienvenida = tk.Frame(root, bg="#222831")
bienvenida.pack()

bienvenida_titulo = tk.Label(bienvenida, text="¡Bienvenido a BarberCos!", font=("Calibri", 22, "bold"), fg="#FFD369", bg="#222831")
bienvenida_titulo.pack(pady=20)

bienvenida_mensaje = tk.Label(bienvenida, text="¿Quiere reservar una cita?", font=("Calibri", 14), fg="white", bg="#222831")
bienvenida_mensaje.pack(pady=10)

boton_ir_reservas = ttk.Button(bienvenida, text="Reservar ahora", command=ir_a_reservas)
boton_ir_reservas.pack(pady=15)

# Pantalla de reservas
pantalla_reservas = tk.Frame(root, bg="#222831")

# Estilos
style = ttk.Style()
style.configure("TButton", font=("Calibri", 14, "bold"), padding=6, background="#FFD369")
style.configure("TLabel", font=("Calibri", 13, "bold"), background="#222831", foreground="#EEEEEE")
style.configure("TMenubutton", font=("Calibri", 12), background="#393E46", foreground="white")

# Título
titulo_reservas = tk.Label(pantalla_reservas, text="BarberCos", font=("Calibri", 22, "bold"), fg="#FFD369", bg="#222831")
titulo_reservas.pack(pady=10)

# Selección de mes
tk.Label(pantalla_reservas, text="Selecciona un mes:", bg="#222831", fg="white", font=("Calibri", 13)).pack()
mes_var = tk.StringVar(root)
meses = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
mes_menu = ttk.OptionMenu(pantalla_reservas, mes_var, "Marzo", *meses.keys(), command=lambda x: actualizar_dias())
mes_menu.pack(pady=5)
mes_var.set("Marzo")

# Selección de día
tk.Label(pantalla_reservas, text="Selecciona un día:", bg="#222831", fg="white", font=("Calibri", 13)).pack()
dia_var = tk.StringVar(root)
dia_menu = ttk.OptionMenu(pantalla_reservas, dia_var, "")
dia_menu.pack(pady=5)

# Selección de hora
tk.Label(pantalla_reservas, text="Selecciona una hora:", bg="#222831", fg="white", font=("Calibri", 13)).pack()
hora_var = tk.StringVar(root)
hora_menu = ttk.OptionMenu(pantalla_reservas, hora_var, "")
hora_menu.pack(pady=5)

# Botón de reserva
boton_reserva = ttk.Button(pantalla_reservas, text="Reservar Cita", command=reservar_cita)
boton_reserva.pack(pady=15)

root.mainloop()