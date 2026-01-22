from tkinter import Tk, Label, Button, Entry, Frame, messagebox, Toplevel, Text, Scrollbar, Listbox
from modules import storage, logic

def ventana_admin():
    admin_win = Tk()
    admin_win.title("Panel de Administrador")
    admin_win.geometry("800x600")

    Label(admin_win, text="PANEL DE ADMINISTRADOR", font=("Arial", 16, "bold")).pack(pady=20)
    frame_botones = Frame(admin_win)
    frame_botones.pack(pady=10)

    Button(frame_botones, text="Gestión de Cooperativas", 
           command=ventana_gestion_cooperativas, width=25, height=2).grid(row=0, column=0, padx=10, pady=10)
    Button(frame_botones, text="Gestión de Rutas", 
           command=ventana_gestion_rutas, width=25, height=2).grid(row=0, column=1, padx=10, pady=10)
    Button(frame_botones, text="Ver Reportes", 
           command=ventana_reportes, width=25, height=2).grid(row=1, column=0, padx=10, pady=10)
    Button(frame_botones, text="Ver Todos los Usuarios", 
           command=mostrar_usuarios, width=25, height=2).grid(row=1, column=1, padx=10, pady=10)
    Button(frame_botones, text="Salir", 
           command=admin_win.destroy, width=25, height=2).grid(row=2, column=0, columnspan=2, pady=20)

    admin_win.mainloop()

def ventana_gestion_cooperativas():
    ventana = Toplevel()
    ventana.title("Gestión de Cooperativas")
    ventana.geometry("600x500")

    Label(ventana, text="GESTIÓN DE COOPERATIVAS", font=("Arial", 14, "bold")).pack(pady=10)
    frame_lista = Frame(ventana)
    frame_lista.pack(pady=10, fill="both", expand=True)
    
    scrollbar = Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")
    
    lista_cooperativas = Listbox(frame_lista, yscrollcommand=scrollbar.set, width=50, height=15)
    for coop in storage.cooperativas:
        lista_cooperativas.insert("end", f"{coop['id']}: {coop['nombre']} - {coop['ciudad']}")
    lista_cooperativas.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=lista_cooperativas.yview)

    def agregar_cooperativa():
        v_agg = Toplevel()
        v_agg.title("Agregar Cooperativa")
        
        Label(v_agg, text="Nombre:").grid(row=0, column=0, pady=5)
        entry_nombre = Entry(v_agg)
        entry_nombre.grid(row=0, column=1, pady=5)
        
        Label(v_agg, text="Ciudad:").grid(row=1, column=0, pady=5)
        entry_ciudad = Entry(v_agg)
        entry_ciudad.grid(row=1, column=1, pady=5)
        
        Label(v_agg, text="Teléfono:").grid(row=2, column=0, pady=5)
        entry_tel = Entry(v_agg)
        entry_tel.grid(row=2, column=1, pady=5)
        
        def guardar():
            nuevo_id = len(storage.cooperativas) + 1
            storage.cooperativas.append({
                "id": nuevo_id,
                "nombre": entry_nombre.get(),
                "ciudad": entry_ciudad.get(),
                "telefono": entry_tel.get(),
                "buses": []
            })
            storage.guardar_datos()
            messagebox.showinfo("Éxito", "Cooperativa agregada")
            v_agg.destroy()
            ventana.destroy() 
            ventana_gestion_cooperativas() # Recargar
        
        Button(v_agg, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)

    def eliminar_cooperativa_sel(lista):
        seleccion = lista.curselection()
        if seleccion:
            indice = seleccion[0]
            storage.cooperativas.pop(indice)
            storage.guardar_datos()
            lista.delete(indice)
            messagebox.showinfo("Éxito", "Cooperativa eliminada")

    frame_botones = Frame(ventana)
    frame_botones.pack(pady=10)
    Button(frame_botones, text="Agregar Cooperativa", command=agregar_cooperativa).pack(side="left", padx=5)
    Button(frame_botones, text="Eliminar Seleccionada", command=lambda: eliminar_cooperativa_sel(lista_cooperativas)).pack(side="left", padx=5)
    Button(frame_botones, text="Cerrar", command=ventana.destroy).pack(side="left", padx=5)

def ventana_gestion_rutas():
    ventana = Toplevel()
    ventana.title("Gestión de Rutas")
    ventana.geometry("700x600")

    Label(ventana, text="GESTIÓN DE RUTAS Y GRAFOS", font=("Arial", 14, "bold")).pack(pady=10)
    frame_agregar = Frame(ventana)
    frame_agregar.pack(pady=10)
    
    Label(frame_agregar, text="Origen:").grid(row=0, column=0)
    entry_origen = Entry(frame_agregar)
    entry_origen.grid(row=0, column=1, padx=5)
    
    Label(frame_agregar, text="Destino:").grid(row=0, column=2)
    entry_destino = Entry(frame_agregar)
    entry_destino.grid(row=0, column=3, padx=5)
    
    Label(frame_agregar, text="Costo:").grid(row=0, column=4)
    entry_costo = Entry(frame_agregar)
    entry_costo.grid(row=0, column=5, padx=5)
    
    def agregar_ruta_grafo():
        origen = entry_origen.get().strip()
        destino = entry_destino.get().strip()
        try:
            costo = float(entry_costo.get())
        except:
            messagebox.showerror("Error", "Costo debe ser un número")
            return
        
        if origen and destino and costo > 0:
            storage.rutas.append({
                "id": len(storage.rutas) + 1,
                "origen": origen,
                "destino": destino,
                "costo": costo
            })
            storage.reconstruir_grafo()
            storage.guardar_datos()
            messagebox.showinfo("Éxito", "Ruta agregada")
            
            texto_grafo.delete(1.0, "end")
            for ciudad, conexiones in storage.grafo_rutas.items():
                texto_grafo.insert("end", f"{ciudad}: {conexiones}\n")
    
    Button(frame_agregar, text="Agregar Ruta", command=agregar_ruta_grafo).grid(row=1, column=0, columnspan=6, pady=10)

    Label(ventana, text="Grafo de Rutas:").pack(pady=5)
    frame_grafo = Frame(ventana)
    frame_grafo.pack(pady=10, fill="both", expand=True)
    texto_grafo = Text(frame_grafo, height=10)
    texto_grafo.pack(side="left", fill="both", expand=True)
    
    for ciudad, conexiones in storage.grafo_rutas.items():
        texto_grafo.insert("end", f"{ciudad}: {conexiones}\n")

    # Búsqueda (Prueba)
    frame_busqueda = Frame(ventana)
    frame_busqueda.pack(pady=10)
    Label(frame_busqueda, text="Prueba - De:").grid(row=0, column=0)
    entry_bo = Entry(frame_busqueda, width=15)
    entry_bo.grid(row=0, column=1)
    Label(frame_busqueda, text="A:").grid(row=0, column=2)
    entry_bd = Entry(frame_busqueda, width=15)
    entry_bd.grid(row=0, column=3)

    def buscar_rutas():
        origen = entry_bo.get().strip()
        destino = entry_bd.get().strip()
        ruta_corta, distancia = logic.dijkstra(origen, destino, storage.grafo_rutas)
        
        res = f"Ruta más corta: {ruta_corta} (Dist: {distancia})" if ruta_corta else "No encontrada"
        messagebox.showinfo("Resultado Dijkstra", res)

    Button(frame_busqueda, text="Probar Dijkstra", command=buscar_rutas).grid(row=1, column=0, columnspan=4, pady=5)

def ventana_reportes():
    ventana = Toplevel()
    ventana.title("Reportes")
    texto = Text(ventana, width=70, height=20)
    texto.pack(pady=10)
    
    texto.insert("end", f"Total usuarios: {len(storage.usuarios)}\n")
    texto.insert("end", f"Total rutas: {len(storage.rutas)}\n")
    texto.insert("end", f"Total tickets: {len(storage.tickets)}\n")
    ingresos = sum(t['precio'] for t in storage.tickets)
    texto.insert("end", f"Ingresos totales: ${ingresos:.2f}\n")

def mostrar_usuarios():
    ventana = Toplevel()
    texto = Text(ventana, width=50, height=20)
    texto.pack(pady=10)
    for u in storage.usuarios:
        texto.insert("end", f"{u['usuario']} ({u['tipo']})\n")