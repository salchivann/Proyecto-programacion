from tkinter import Tk, Label, Button, Entry, Frame, messagebox, Toplevel, Canvas, Text, Scrollbar, Listbox, StringVar
from datetime import datetime
from modules import storage, logic

def ventana_pasajero(nombre_pasajero):
    pasajero_win = Tk()
    pasajero_win.title(f"Pasajero: {nombre_pasajero}")
    pasajero_win.geometry("800x700")

    Label(pasajero_win, text=f"Hola, {nombre_pasajero}", font=("Arial", 14)).pack(pady=10)

    Button(pasajero_win, text="Buscar Ruta", command=lambda: ventana_seleccion_ruta(nombre_pasajero)).pack(pady=5)
    Button(pasajero_win, text="Ver Mis Tickets", command=lambda: ver_tickets(nombre_pasajero)).pack(pady=5)
    Button(pasajero_win, text="Salir", command=pasajero_win.destroy).pack(pady=20)
    
    pasajero_win.mainloop()

def ventana_seleccion_ruta(nombre_pasajero):
    ventana = Toplevel()
    ventana.title("Buscar")
    
    Label(ventana, text="Origen:").pack()
    e_origen = Entry(ventana)
    e_origen.pack()
    Label(ventana, text="Destino:").pack()
    e_destino = Entry(ventana)
    e_destino.pack()
    
    res_text = Text(ventana, height=10)
    res_text.pack()
    
    def buscar():
        org = e_origen.get()
        des = e_destino.get()
        rutas = logic.buscar_rutas_recursivo(org, des, storage.grafo_rutas, [], 0, 5)
        res_text.delete(1.0, "end")
        if not rutas:
            res_text.insert("end", "No hay rutas")
        else:
            for r in rutas:
                precio = logic.calcular_precio_recursivo(r, storage.grafo_rutas)
                res_text.insert("end", f"Ruta: {'->'.join(r)} (${precio})\n")
                
                # Buscamos buses directos para simplificar
                buses_directos = [b for b in storage.buses if org in b['ruta'] and des in b['ruta']]
                if buses_directos:
                    res_text.insert("end", f"  -> Buses disponibles: {[b['id'] for b in buses_directos]}\n")

    Button(ventana, text="Buscar", command=buscar).pack()

    Label(ventana, text="ID Bus a comprar:").pack()
    e_id = Entry(ventana)
    e_id.pack()
    
    def ir_a_asientos():
        try:
            bid = int(e_id.get())
            ventana_seleccion_asiento(bid, nombre_pasajero)
        except:
            pass
            
    Button(ventana, text="Seleccionar Asientos", command=ir_a_asientos).pack()

def ventana_seleccion_asiento(bus_id, nombre_pasajero):
    ventana = Toplevel()
    ventana.title(f"Asientos Bus {bus_id}")
    
    bus = next((b for b in storage.buses if b['id'] == bus_id), None)
    if not bus: return
    
    canvas = Canvas(ventana, width=400, height=400, bg="white")
    canvas.pack()
    
    sz = 40
    
    def comprar(f, c):
        if logic.reservar_asiento(bus['asientos'], f, c):
            storage.tickets.append({
                "id": len(storage.tickets)+1,
                "pasajero": nombre_pasajero,
                "bus_id": bus_id,
                "ruta": bus["ruta"],
                "asiento": f"{f+1}-{c+1}",
                "precio": bus["precio_base"],
                "fecha_compra": str(datetime.now())
            })
            storage.historial_compras.append({"pasajero": nombre_pasajero, "accion": "compra", "fecha": str(datetime.now())})
            storage.guardar_datos()
            messagebox.showinfo("Éxito", "Ticket comprado")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Ocupado")

    for r in range(len(bus['asientos'])):
        for c in range(len(bus['asientos'][0])):
            color = "green" if bus['asientos'][r][c] == "L" else "red"
            id_rect = canvas.create_rectangle(50+c*sz, 50+r*sz, 50+c*sz+sz, 50+r*sz+sz, fill=color)
            canvas.tag_bind(id_rect, "<Button-1>", lambda e, row=r, col=c: comprar(row, col))

def ver_tickets(nombre):
    ventana = Toplevel()
    tcks = [t for t in storage.tickets if t['pasajero'] == nombre]
    lb = Listbox(ventana, width=50)
    lb.pack()
    for t in tcks:
        lb.insert("end", f"#{t['id']} - {t['ruta']} - {t['asiento']}")