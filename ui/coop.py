from tkinter import Tk, Label, Button, Entry, Frame, messagebox, Toplevel, Canvas, Text, Scrollbar, Listbox, StringVar, OptionMenu
from modules import storage, logic

def ventana_cooperativa(nombre_coop):
    coop_win = Tk()
    coop_win.title(f"Panel: {nombre_coop}")
    coop_win.geometry("700x600")

    Label(coop_win, text=f"PANEL COOPERATIVA: {nombre_coop}", font=("Arial", 14, "bold")).pack(pady=20)
    frame_botones = Frame(coop_win)
    frame_botones.pack(pady=10)

    Button(frame_botones, text="Gestión de Horarios", 
           command=lambda: ventana_gestion_horarios(nombre_coop), width=25, height=2).grid(row=0, column=0, padx=10, pady=10)
    Button(frame_botones, text="Gestión de Asientos", 
           command=lambda: ventana_gestion_asientos(nombre_coop), width=25, height=2).grid(row=0, column=1, padx=10, pady=10)
    Button(frame_botones, text="Salir", 
           command=coop_win.destroy, width=25, height=2).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    coop_win.mainloop()

def ventana_gestion_horarios(nombre_coop):
    ventana = Toplevel()
    ventana.title("Horarios")
    
    Label(ventana, text="Ruta (Origen-Destino):").pack()
    entry_ruta = Entry(ventana)
    entry_ruta.pack()
    
    Label(ventana, text="Hora Salida:").pack()
    entry_hora = Entry(ventana)
    entry_hora.pack()
    
    Label(ventana, text="Precio:").pack()
    entry_precio = Entry(ventana)
    entry_precio.pack()
    
    def agregar():
        try:
            p = float(entry_precio.get())
            nuevo = {
                "id": len(storage.buses) + 1,
                "cooperativa": nombre_coop,
                "ruta": entry_ruta.get(),
                "hora_salida": entry_hora.get(),
                "hora_llegada": "?",
                "precio_base": p,
                "asientos": logic.crear_matriz_asientos(),
                "asientos_disponibles": 40
            }
            storage.buses.append(nuevo)
            storage.guardar_datos()
            messagebox.showinfo("Éxito", "Bus agregado")
            ventana.destroy()
        except:
            messagebox.showerror("Error", "Datos inválidos")

    Button(ventana, text="Guardar", command=agregar).pack(pady=10)

def ventana_gestion_asientos(nombre_coop):
    ventana = Toplevel()
    ventana.title("Gestión Asientos")
    
    buses_coop = [b for b in storage.buses if b["cooperativa"] == nombre_coop]
    if not buses_coop:
        Label(ventana, text="No hay buses").pack()
        return

    bus_var = StringVar(ventana)
    bus_var.set(f"Bus {buses_coop[0]['id']}")
    opciones = [f"Bus {b['id']}" for b in buses_coop]
    OptionMenu(ventana, bus_var, *opciones).pack(pady=5)
    
    canvas = Canvas(ventana, width=400, height=400, bg="white")
    canvas.pack()
    
    def dibujar():
        canvas.delete("all")
        bid = int(bus_var.get().split(" ")[1])
        bus = next((b for b in storage.buses if b["id"] == bid), None)
        if not bus: return
        
        matriz = bus["asientos"]
        sz = 30
        for r in range(len(matriz)):
            for c in range(len(matriz[0])):
                color = "green" if matriz[r][c] == "L" else "red"
                canvas.create_rectangle(50+c*sz, 50+r*sz, 50+c*sz+sz, 50+r*sz+sz, fill=color)
    
    Button(ventana, text="Ver Mapa", command=dibujar).pack()