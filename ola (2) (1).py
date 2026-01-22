from tkinter import Tk, Label, Button, Entry, Frame, messagebox, Toplevel, Canvas, Text, Scrollbar, Listbox, StringVar, OptionMenu
from PIL import Image, ImageTk
import json
import os
from datetime import datetime
from collections import deque
import itertools

# ESTRUCTURAS DE DATOS GLOBALES (LISTAS Y MATRICES) ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
usuarios = []  # Lista para usuarios
cooperativas = []  # Lista para cooperativas
rutas = []  # Lista para rutas
buses = []  # Lista para buses con matrices de asientos
tickets = []  # Lista para tickets vendidos
grafo_rutas = {}  # Grafo para las conexiones entre ciudades
historial_compras = []  # Lista para historial recursivo

# MANEJO DE ARCHIVOS (FICHEROS JSON) ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
ARCHIVO_USUARIOS = "data/usuarios.json"
ARCHIVO_COOPERATIVAS = "data/cooperativas.json"
ARCHIVO_RUTAS = "data/rutas.json"
ARCHIVO_BUSES = "data/buses.json"
ARCHIVO_TICKETS = "data/tickets.json"

def crear_directorios():
    """Crea los directorios necesarios para los archivos"""
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

def cargar_datos():
    """Carga todos los datos desde los archivos JSON"""
    global usuarios, cooperativas, rutas, buses, tickets, grafo_rutas
    
    try:
        if os.path.exists(ARCHIVO_USUARIOS):
            with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
        
        if os.path.exists(ARCHIVO_COOPERATIVAS):
            with open(ARCHIVO_COOPERATIVAS, 'r', encoding='utf-8') as f:
                cooperativas = json.load(f)
        
        if os.path.exists(ARCHIVO_RUTAS):
            with open(ARCHIVO_RUTAS, 'r', encoding='utf-8') as f:
                rutas = json.load(f)
                # Construir grafo a partir de rutas
                for ruta in rutas:
                    origen = ruta['origen']
                    destino = ruta['destino']
                    costo = ruta['costo']
                    
                    if origen not in grafo_rutas:
                        grafo_rutas[origen] = []
                    if destino not in grafo_rutas:
                        grafo_rutas[destino] = []
                    
                    grafo_rutas[origen].append((destino, costo))
                    grafo_rutas[destino].append((origen, costo))
        
        if os.path.exists(ARCHIVO_BUSES):
            with open(ARCHIVO_BUSES, 'r', encoding='utf-8') as f:
                buses = json.load(f)
        
        if os.path.exists(ARCHIVO_TICKETS):
            with open(ARCHIVO_TICKETS, 'r', encoding='utf-8') as f:
                tickets = json.load(f)
                
    except Exception as e:
        print(f"Error cargando datos: {e}")

def guardar_datos():
    """Guarda todos los datos en archivos JSON"""
    try:
        with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=2)
        
        with open(ARCHIVO_COOPERATIVAS, 'w', encoding='utf-8') as f:
            json.dump(cooperativas, f, indent=2)
        
        with open(ARCHIVO_RUTAS, 'w', encoding='utf-8') as f:
            json.dump(rutas, f, indent=2)
        
        with open(ARCHIVO_BUSES, 'w', encoding='utf-8') as f:
            json.dump(buses, f, indent=2)
        
        with open(ARCHIVO_TICKETS, 'w', encoding='utf-8') as f:
            json.dump(tickets, f, indent=2)
            
    except Exception as e:
        print(f"Error guardando datos: {e}")

# FUNCIONES DE GRAFOS ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
def dijkstra(origen, destino):
    """Algoritmo de Dijkstra para encontrar la ruta más corta"""
    if origen not in grafo_rutas or destino not in grafo_rutas:
        return None, float('inf')
    
    distancias = {ciudad: float('inf') for ciudad in grafo_rutas}
    distancias[origen] = 0
    previos = {ciudad: None for ciudad in grafo_rutas}
    visitados = set()
    
    while len(visitados) < len(distancias):
        # Encontrar ciudad no visitada con menor distancia
        ciudad_actual = None
        min_distancia = float('inf')
        
        for ciudad in grafo_rutas:
            if ciudad not in visitados and distancias[ciudad] < min_distancia:
                min_distancia = distancias[ciudad]
                ciudad_actual = ciudad
        
        if ciudad_actual is None or ciudad_actual == destino:
            break
        
        visitados.add(ciudad_actual)
        
        # Actualizar distancias de vecinos
        for vecino, costo in grafo_rutas[ciudad_actual]:
            nueva_distancia = distancias[ciudad_actual] + costo
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                previos[vecino] = ciudad_actual
    
    # Reconstruir ruta
    ruta = []
    actual = destino
    while actual is not None:
        ruta.insert(0, actual)
        actual = previos[actual]
    
    if ruta[0] != origen:
        return None, float('inf')
    
    return ruta, distancias[destino]

def buscar_todas_rutas(origen, destino, visitados=None, ruta_actual=None):
    """Función RECURSIVA para encontrar todas las rutas posibles"""
    if visitados is None:
        visitados = set()
    if ruta_actual is None:
        ruta_actual = []
    
    visitados.add(origen)
    ruta_actual.append(origen)
    
    rutas_encontradas = []
    
    if origen == destino:
        rutas_encontradas.append(list(ruta_actual))
    else:
        for vecino, _ in grafo_rutas.get(origen, []):
            if vecino not in visitados:
                rutas_recursivas = buscar_todas_rutas(vecino, destino, visitados.copy(), list(ruta_actual))
                rutas_encontradas.extend(rutas_recursivas)
    
    return rutas_encontradas

def rutas_mas_economica_cara(origen, destino):
    """Encuentra la ruta más económica y más cara"""
    todas_rutas = buscar_todas_rutas(origen, destino)
    
    if not todas_rutas:
        return None, None, 0, 0
    
    mejor_ruta = None
    peor_ruta = None
    menor_costo = float('inf')
    mayor_costo = 0
    
    for ruta in todas_rutas:
        costo_total = 0
        for i in range(len(ruta) - 1):
            for vecino, costo in grafo_rutas[ruta[i]]:
                if vecino == ruta[i + 1]:
                    costo_total += costo
                    break
        
        if costo_total < menor_costo:
            menor_costo = costo_total
            mejor_ruta = ruta
        
        if costo_total > mayor_costo:
            mayor_costo = costo_total
            peor_ruta = ruta
    
    return mejor_ruta, peor_ruta, menor_costo, mayor_costo

# FUNCIONES DE MATRICES (ASIENTOS) ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
def crear_matriz_asientos(filas=10, columnas=4):
    """Crea una matriz de asientos vacía"""
    return [['L' for _ in range(columnas)] for _ in range(filas)]

def contar_asientos_disponibles(matriz):
    """Cuenta los asientos disponibles en la matriz"""
    disponibles = 0
    for fila in matriz:
        for asiento in fila:
            if asiento == 'L':
                disponibles += 1
    return disponibles

def reservar_asiento(matriz, fila, columna):
    """Reserva un asiento en la matriz"""
    if 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0]):
        if matriz[fila][columna] == 'L':
            matriz[fila][columna] = 'R'
            return True
    return False

def mostrar_matriz_asientos(matriz):
    """Muestra la matriz de asientos en formato texto"""
    resultado = "   "
    for col in range(len(matriz[0])):
        resultado += f" {col+1}  "
    resultado += "\n"
    
    for i, fila in enumerate(matriz):
        resultado += f"{i+1:2} "
        for asiento in fila:
            if asiento == 'L':
                resultado += "[ ] "
            else:
                resultado += "[X] "
        resultado += "\n"
    return resultado

# FUNCIONES RECURSIVAS (ÁRBOL DE BÚSQUEDA) ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
def buscar_rutas_recursivo(ciudad_actual, destino, visitadas, profundidad, max_profundidad=3):
    """Búsqueda recursiva de rutas con límite de profundidad"""
    if profundidad > max_profundidad:
        return []
    
    if ciudad_actual == destino:
        return [[ciudad_actual]]
    
    visitadas.append(ciudad_actual)
    rutas = []
    
    for vecino, _ in grafo_rutas.get(ciudad_actual, []):
        if vecino not in visitadas:
            rutas_parciales = buscar_rutas_recursivo(vecino, destino, visitadas.copy(), profundidad + 1, max_profundidad)
            for ruta in rutas_parciales:
                rutas.append([ciudad_actual] + ruta)
    
    return rutas

def calcular_precio_recursivo(ruta, indice=0):
    """Calcula precio recursivamente para una ruta"""
    if indice >= len(ruta) - 1:
        return 0
    
    ciudad_actual = ruta[indice]
    siguiente = ruta[indice + 1]
    
    for vecino, costo in grafo_rutas.get(ciudad_actual, []):
        if vecino == siguiente:
            return costo + calcular_precio_recursivo(ruta, indice + 1)
    
    return 0

# VENTANA DE REGISTRO (MEJORADA) ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
def abrir_registro(root):
    nueva_ventana = Toplevel(root)
    nueva_ventana.title("Registro")
    nueva_ventana.geometry("400x400")

    Label(nueva_ventana, text="REGISTRAR NUEVO USUARIO", font=("Arial", 14, "bold")).pack(pady=10)

    frame_campos = Frame(nueva_ventana)
    frame_campos.pack(pady=10)

    Label(frame_campos, text="Nuevo usuario:").grid(row=0, column=0, pady=5, sticky="e")
    entry_user = Entry(frame_campos, width=25)
    entry_user.grid(row=0, column=1, pady=5)

    Label(frame_campos, text="Nueva contraseña:").grid(row=1, column=0, pady=5, sticky="e")
    entry_contra = Entry(frame_campos, show="*", width=25)
    entry_contra.grid(row=1, column=1, pady=5)

    Label(frame_campos, text="Tipo de usuario:").grid(row=2, column=0, pady=5, sticky="e")
    tipo_var = StringVar(nueva_ventana)
    tipo_var.set("pasajero")
    OptionMenu(frame_campos, tipo_var, "pasajero", "cooperativa", "admin").grid(row=2, column=1, pady=5)

    def guardar_usuario():
        nuevo_usuario = entry_user.get().strip()
        nueva_contra = entry_contra.get().strip()
        tipo = tipo_var.get()

        if not nuevo_usuario or not nueva_contra:
            messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos")
            return

        for u in usuarios:
            if u["usuario"] == nuevo_usuario:
                messagebox.showerror("Error", "Ese usuario ya existe")
                return

        usuarios.append({
            "usuario": nuevo_usuario,
            "contraseña": nueva_contra,
            "tipo": tipo
        })
        
        guardar_datos()
        messagebox.showinfo("Éxito", f"Usuario {tipo} registrado correctamente")
        nueva_ventana.destroy()

    frame_botones = Frame(nueva_ventana)
    frame_botones.pack(pady=20)

    Button(frame_botones, text="Guardar", command=guardar_usuario, width=15).pack(pady=5)
    Button(frame_botones, text="Cerrar", command=nueva_ventana.destroy, width=15).pack(pady=5)

# FUNCIÓN PARA INGRESAR ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
def entrar(entry_user, entry_contra, root):
    nombre = entry_user.get().strip()
    contra = entry_contra.get().strip()

    if not nombre or not contra:
        messagebox.showwarning("Campos vacíos", "Por favor llena todos los campos")
        return

    for u in usuarios:
        if u["usuario"] == nombre and u["contraseña"] == contra:
            messagebox.showinfo("Acceso correcto", f"Bienvenido {nombre}")
            root.destroy()
            
            # Abrir ventana según tipo de usuario
            if u["tipo"] == "admin":
                ventana_admin()
            elif u["tipo"] == "cooperativa":
                ventana_cooperativa(nombre)
            else:  # pasajero
                ventana_pasajero(nombre)
            return

    messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")

# VENTANA DE ADMINISTRADOR ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
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

    # Lista de cooperativas
    frame_lista = Frame(ventana)
    frame_lista.pack(pady=10, fill="both", expand=True)
    
    scrollbar = Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")
    
    lista_cooperativas = Listbox(frame_lista, yscrollcommand=scrollbar.set, width=50, height=15)
    for coop in cooperativas:
        lista_cooperativas.insert("end", f"{coop['id']}: {coop['nombre']} - {coop['ciudad']}")
    lista_cooperativas.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=lista_cooperativas.yview)

    # Botones de gestión
    frame_botones = Frame(ventana)
    frame_botones.pack(pady=10)

    Button(frame_botones, text="Agregar Cooperativa", command=agregar_cooperativa).pack(side="left", padx=5)
    Button(frame_botones, text="Eliminar Seleccionada", 
           command=lambda: eliminar_cooperativa(lista_cooperativas)).pack(side="left", padx=5)
    Button(frame_botones, text="Cerrar", command=ventana.destroy).pack(side="left", padx=5)

def agregar_cooperativa():
    ventana = Toplevel()
    ventana.title("Agregar Cooperativa")
    
    Label(ventana, text="Nombre:").grid(row=0, column=0, pady=5)
    entry_nombre = Entry(ventana)
    entry_nombre.grid(row=0, column=1, pady=5)
    
    Label(ventana, text="Ciudad:").grid(row=1, column=0, pady=5)
    entry_ciudad = Entry(ventana)
    entry_ciudad.grid(row=1, column=1, pady=5)
    
    Label(ventana, text="Teléfono:").grid(row=2, column=0, pady=5)
    entry_tel = Entry(ventana)
    entry_tel.grid(row=2, column=1, pady=5)
    
    def guardar():
        nuevo_id = len(cooperativas) + 1
        cooperativas.append({
            "id": nuevo_id,
            "nombre": entry_nombre.get(),
            "ciudad": entry_ciudad.get(),
            "telefono": entry_tel.get(),
            "buses": []
        })
        guardar_datos()
        messagebox.showinfo("Éxito", "Cooperativa agregada correctamente")
        ventana.destroy()
    
    Button(ventana, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)

def eliminar_cooperativa(lista):
    seleccion = lista.curselection()
    if seleccion:
        indice = seleccion[0]
        cooperativas.pop(indice)
        guardar_datos()
        lista.delete(indice)
        messagebox.showinfo("Éxito", "Cooperativa eliminada")

def ventana_gestion_rutas():
    ventana = Toplevel()
    ventana.title("Gestión de Rutas")
    ventana.geometry("700x600")

    Label(ventana, text="GESTIÓN DE RUTAS Y GRAFOS", font=("Arial", 14, "bold")).pack(pady=10)

    # Frame para agregar ruta
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
            # Agregar a lista de rutas
            rutas.append({
                "id": len(rutas) + 1,
                "origen": origen,
                "destino": destino,
                "costo": costo
            })
            
            # Actualizar grafo
            if origen not in grafo_rutas:
                grafo_rutas[origen] = []
            if destino not in grafo_rutas:
                grafo_rutas[destino] = []
            
            grafo_rutas[origen].append((destino, costo))
            grafo_rutas[destino].append((origen, costo))
            
            guardar_datos()
            messagebox.showinfo("Éxito", "Ruta agregada al grafo")
            
            # Actualizar visualización
            texto_grafo.delete(1.0, "end")
            for ciudad, conexiones in grafo_rutas.items():
                texto_grafo.insert("end", f"{ciudad}: {conexiones}\n")
    
    Button(frame_agregar, text="Agregar Ruta", command=agregar_ruta_grafo).grid(row=1, column=0, columnspan=6, pady=10)

    # Visualización del grafo
    Label(ventana, text="Grafo de Rutas:").pack(pady=5)
    frame_grafo = Frame(ventana)
    frame_grafo.pack(pady=10, fill="both", expand=True)
    
    scrollbar = Scrollbar(frame_grafo)
    scrollbar.pack(side="right", fill="y")
    
    texto_grafo = Text(frame_grafo, yscrollcommand=scrollbar.set, width=60, height=15)
    texto_grafo.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=texto_grafo.yview)
    
    # Mostrar grafo actual
    for ciudad, conexiones in grafo_rutas.items():
        texto_grafo.insert("end", f"{ciudad}: {conexiones}\n")

    # Búsqueda de rutas
    frame_busqueda = Frame(ventana)
    frame_busqueda.pack(pady=10)
    
    Label(frame_busqueda, text="Buscar ruta de:").grid(row=0, column=0)
    entry_busqueda_origen = Entry(frame_busqueda, width=15)
    entry_busqueda_origen.grid(row=0, column=1, padx=5)
    
    Label(frame_busqueda, text="a:").grid(row=0, column=2)
    entry_busqueda_destino = Entry(frame_busqueda, width=15)
    entry_busqueda_destino.grid(row=0, column=3, padx=5)
    
    def buscar_rutas():
        origen = entry_busqueda_origen.get().strip()
        destino = entry_busqueda_destino.get().strip()
        
        if not origen or not destino:
            messagebox.showwarning("Error", "Ingrese origen y destino")
            return
        
        # Ruta más corta (Dijkstra)
        ruta_corta, distancia = dijkstra(origen, destino)
        
        # Todas las rutas posibles
        todas = buscar_todas_rutas(origen, destino)
        
        # Rutas más económica y cara
        eco, cara, costo_eco, costo_cara = rutas_mas_economica_cara(origen, destino)
        
        # Mostrar resultados
        texto_resultados = Text(ventana, width=70, height=10)
        texto_resultados.pack(pady=10)
        
        texto_resultados.insert("end", f"RUTA MÁS CORTA (Dijkstra):\n")
        if ruta_corta:
            texto_resultados.insert("end", f"  Ruta: {' -> '.join(ruta_corta)}\n")
            texto_resultados.insert("end", f"  Distancia total: {distancia}\n")
        else:
            texto_resultados.insert("end", "  No encontrada\n")
        
        texto_resultados.insert("end", f"\nRUTA MÁS ECONÓMICA:\n")
        if eco:
            texto_resultados.insert("end", f"  Ruta: {' -> '.join(eco)}\n")
            texto_resultados.insert("end", f"  Costo: {costo_eco}\n")
        
        texto_resultados.insert("end", f"\nRUTA MÁS COSTOSA:\n")
        if cara:
            texto_resultados.insert("end", f"  Ruta: {' -> '.join(cara)}\n")
            texto_resultados.insert("end", f"  Costo: {costo_cara}\n")
        
        texto_resultados.insert("end", f"\nTODAS LAS RUTAS POSIBLES ({len(todas)}):\n")
        for i, ruta in enumerate(todas[:5], 1):  # Mostrar solo primeras 5
            costo = calcular_precio_recursivo(ruta)
            texto_resultados.insert("end", f"  {i}. {' -> '.join(ruta)} (Costo: {costo})\n")
        if len(todas) > 5:
            texto_resultados.insert("end", f"  ... y {len(todas)-5} rutas más\n")
    
    Button(frame_busqueda, text="Buscar Rutas", command=buscar_rutas).grid(row=1, column=0, columnspan=4, pady=10)
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

def ventana_reportes():
    ventana = Toplevel()
    ventana.title("Reportes del Sistema")
    ventana.geometry("600x500")
    
    texto = Text(ventana, width=70, height=30)
    texto.pack(pady=10)
    
    # Estadísticas
    texto.insert("end", "=== REPORTE DEL SISTEMA ===\n\n")
    texto.insert("end", f"Total de usuarios: {len(usuarios)}\n")
    texto.insert("end", f"  - Administradores: {sum(1 for u in usuarios if u['tipo'] == 'admin')}\n")
    texto.insert("end", f"  - Cooperativas: {sum(1 for u in usuarios if u['tipo'] == 'cooperativa')}\n")
    texto.insert("end", f"  - Pasajeros: {sum(1 for u in usuarios if u['tipo'] == 'pasajero')}\n\n")
    
    texto.insert("end", f"Total de cooperativas: {len(cooperativas)}\n")
    texto.insert("end", f"Total de rutas: {len(rutas)}\n")
    texto.insert("end", f"Total de buses: {len(buses)}\n")
    texto.insert("end", f"Total de tickets vendidos: {len(tickets)}\n\n")
    
    # Ingresos totales
    ingresos = sum(t['precio'] for t in tickets)
    texto.insert("end", f"Ingresos totales: ${ingresos:.2f}\n")
    
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

def mostrar_usuarios():
    ventana = Toplevel()
    ventana.title("Lista de Usuarios")
    
    texto = Text(ventana, width=50, height=20)
    texto.pack(pady=10)
    
    for usuario in usuarios:
        texto.insert("end", f"Usuario: {usuario['usuario']}\n")
        texto.insert("end", f"  Tipo: {usuario['tipo']}\n")
        texto.insert("end", "-" * 40 + "\n")
    
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

# VENTANA DE COOPERATIVA ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
def ventana_cooperativa(nombre_coop):
    coop_win = Tk()
    coop_win.title(f"Panel de Cooperativa: {nombre_coop}")
    coop_win.geometry("700x600")

    Label(coop_win, text=f"PANEL DE COOPERATIVA: {nombre_coop}", font=("Arial", 14, "bold")).pack(pady=20)

    frame_botones = Frame(coop_win)
    frame_botones.pack(pady=10)

    Button(frame_botones, text="Gestión de Horarios", 
           command=lambda: ventana_gestion_horarios(nombre_coop), width=25, height=2).grid(row=0, column=0, padx=10, pady=10)
    Button(frame_botones, text="Gestión de Asientos", 
           command=lambda: ventana_gestion_asientos(nombre_coop), width=25, height=2).grid(row=0, column=1, padx=10, pady=10)
    Button(frame_botones, text="Ver Mis Buses", 
           command=lambda: mostrar_buses_coop(nombre_coop), width=25, height=2).grid(row=1, column=0, padx=10, pady=10)
    Button(frame_botones, text="Salir", 
           command=coop_win.destroy, width=25, height=2).grid(row=1, column=1, padx=10, pady=10)

    coop_win.mainloop()

def ventana_gestion_horarios(nombre_coop):
    ventana = Toplevel()
    ventana.title("Gestión de Horarios")
    ventana.geometry("600x500")
    
    Label(ventana, text="GESTIÓN DE HORARIOS DE BUSES", font=("Arial", 14, "bold")).pack(pady=10)
    
    # Formulario para agregar bus/horario
    frame_form = Frame(ventana)
    frame_form.pack(pady=10)
    
    Label(frame_form, text="Ruta (Origen-Destino):").grid(row=0, column=0, pady=5)
    entry_ruta = Entry(frame_form)
    entry_ruta.grid(row=0, column=1, pady=5)
    
    Label(frame_form, text="Hora Salida (HH:MM):").grid(row=1, column=0, pady=5)
    entry_hora_salida = Entry(frame_form)
    entry_hora_salida.grid(row=1, column=1, pady=5)
    
    Label(frame_form, text="Hora Llegada (HH:MM):").grid(row=2, column=0, pady=5)
    entry_hora_llegada = Entry(frame_form)
    entry_hora_llegada.grid(row=2, column=1, pady=5)
    
    Label(frame_form, text="Precio Base:").grid(row=3, column=0, pady=5)
    entry_precio = Entry(frame_form)
    entry_precio.grid(row=3, column=1, pady=5)
    
    def agregar_bus():
        # Crear matriz de asientos para el bus
        asientos_matriz = crear_matriz_asientos()
        
        nuevo_bus = {
            "id": len(buses) + 1,
            "cooperativa": nombre_coop,
            "ruta": entry_ruta.get(),
            "hora_salida": entry_hora_salida.get(),
            "hora_llegada": entry_hora_llegada.get(),
            "precio_base": float(entry_precio.get()),
            "asientos": asientos_matriz,
            "asientos_disponibles": 40  # 10x4 = 40 asientos
        }
        
        buses.append(nuevo_bus)
        guardar_datos()
        messagebox.showinfo("Éxito", "Bus/horario agregado correctamente")
        ventana.destroy()
    
    Button(frame_form, text="Agregar Bus/Horario", command=agregar_bus).grid(row=4, column=0, columnspan=2, pady=10)
    
    # Mostrar buses existentes de esta cooperativa
    Label(ventana, text="Buses de esta cooperativa:").pack(pady=10)
    
    frame_lista = Frame(ventana)
    frame_lista.pack(pady=10, fill="both", expand=True)
    
    scrollbar = Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")
    
    lista_buses = Listbox(frame_lista, yscrollcommand=scrollbar.set, width=60, height=10)
    for bus in buses:
        if bus["cooperativa"] == nombre_coop:
            lista_buses.insert("end", f"Bus {bus['id']}: {bus['ruta']} | Salida: {bus['hora_salida']} | Precio: ${bus['precio_base']}")
    lista_buses.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=lista_buses.yview)
    
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

def ventana_gestion_asientos(nombre_coop):
    ventana = Toplevel()
    ventana.title("Gestión de Asientos")
    ventana.geometry("700x600")
    
    Label(ventana, text="GESTIÓN DE ASIENTOS - MATRIZ VISUAL", font=("Arial", 14, "bold")).pack(pady=10)
    
    # Seleccionar bus
    Label(ventana, text="Seleccionar Bus:").pack(pady=5)
    
    buses_coop = [b for b in buses if b["cooperativa"] == nombre_coop]
    bus_var = StringVar(ventana)
    
    if buses_coop:
        bus_var.set(f"Bus {buses_coop[0]['id']}: {buses_coop[0]['ruta']}")
        opciones = [f"Bus {b['id']}: {b['ruta']}" for b in buses_coop]
    else:
        bus_var.set("No hay buses")
        opciones = ["No hay buses"]
    
    OptionMenu(ventana, bus_var, *opciones).pack(pady=5)
    
    # Canvas para mostrar matriz de asientos
    canvas = Canvas(ventana, width=400, height=400, bg="white")
    canvas.pack(pady=10)
    
    def dibujar_matriz():
        canvas.delete("all")
        
        # Encontrar bus seleccionado
        seleccion = bus_var.get()
        if seleccion == "No hay buses":
            return
        
        bus_id = int(seleccion.split(" ")[1].split(":")[0])
        bus = next((b for b in buses if b["id"] == bus_id), None)
        
        if not bus:
            return
        
        matriz = bus["asientos"]
        filas = len(matriz)
        columnas = len(matriz[0])
        
        # Dibujar matriz
        cell_size = 30
        start_x = 50
        start_y = 50
        
        # Dibujar números de columnas
        for col in range(columnas):
            x = start_x + col * cell_size + cell_size//2
            canvas.create_text(x, start_y - 20, text=str(col+1))
        
        for fila in range(filas):
            # Dibujar número de fila
            canvas.create_text(start_x - 20, start_y + fila * cell_size + cell_size//2, text=str(fila+1))
            
            for col in range(columnas):
                x1 = start_x + col * cell_size
                y1 = start_y + fila * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                if matriz[fila][col] == 'L':  # Libre
                    canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="black")
                    canvas.create_text((x1+x2)//2, (y1+y2)//2, text="L")
                else:  # Reservado
                    canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")
                    canvas.create_text((x1+x2)//2, (y1+y2)//2, text="R")
        
        # Mostrar estadísticas
        disponibles = contar_asientos_disponibles(matriz)
        Label(ventana, text=f"Asientos disponibles: {disponibles} / {filas*columnas}").pack()
    
    Button(ventana, text="Actualizar Vista", command=dibujar_matriz).pack(pady=5)
    
    # Reservar asiento manualmente
    frame_reserva = Frame(ventana)
    frame_reserva.pack(pady=10)
    
    Label(frame_reserva, text="Reservar asiento - Fila:").grid(row=0, column=0)
    entry_fila = Entry(frame_reserva, width=5)
    entry_fila.grid(row=0, column=1, padx=5)
    
    Label(frame_reserva, text="Columna:").grid(row=0, column=2)
    entry_columna = Entry(frame_reserva, width=5)
    entry_columna.grid(row=0, column=3, padx=5)
    
    def reservar_asiento_manual():
        try:
            fila = int(entry_fila.get()) - 1
            col = int(entry_columna.get()) - 1
            
            seleccion = bus_var.get()
            bus_id = int(seleccion.split(" ")[1].split(":")[0])
            bus = next((b for b in buses if b["id"] == bus_id), None)
            
            if bus and reservar_asiento(bus["asientos"], fila, col):
                guardar_datos()
                messagebox.showinfo("Éxito", f"Asiento {fila+1}-{col+1} reservado")
                dibujar_matriz()
            else:
                messagebox.showerror("Error", "Asiento no disponible o coordenadas inválidas")
                
        except ValueError:
            messagebox.showerror("Error", "Ingrese números válidos")
    
    Button(frame_reserva, text="Reservar Asiento", command=reservar_asiento_manual).grid(row=1, column=0, columnspan=4, pady=5)
    
    # Mostrar matriz en texto también
    Label(ventana, text="Representación en Texto:").pack(pady=5)
    texto_matriz = Text(ventana, width=50, height=8)
    texto_matriz.pack(pady=5)
    
    def actualizar_texto():
        seleccion = bus_var.get()
        if seleccion != "No hay buses":
            bus_id = int(seleccion.split(" ")[1].split(":")[0])
            bus = next((b for b in buses if b["id"] == bus_id), None)
            if bus:
                texto_matriz.delete(1.0, "end")
                texto_matriz.insert("end", mostrar_matriz_asientos(bus["asientos"]))
    
    Button(ventana, text="Actualizar Texto", command=actualizar_texto).pack(pady=5)
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    
    # Dibujar matriz inicial
    dibujar_matriz()

def mostrar_buses_coop(nombre_coop):
    ventana = Toplevel()
    ventana.title("Mis Buses")
    
    texto = Text(ventana, width=70, height=20)
    texto.pack(pady=10)
    
    buses_coop = [b for b in buses if b["cooperativa"] == nombre_coop]
    
    if not buses_coop:
        texto.insert("end", "No tienes buses registrados.\n")
    else:
        for bus in buses_coop:
            texto.insert("end", f"Bus ID: {bus['id']}\n")
            texto.insert("end", f"  Ruta: {bus['ruta']}\n")
            texto.insert("end", f"  Horario: {bus['hora_salida']} - {bus['hora_llegada']}\n")
            texto.insert("end", f"  Precio: ${bus['precio_base']:.2f}\n")
            disponibles = contar_asientos_disponibles(bus['asientos'])
            texto.insert("end", f"  Asientos disponibles: {disponibles}/40\n")
            texto.insert("end", "-" * 50 + "\n")
    
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

# VENTANA DE PASAJERO ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
def ventana_pasajero(nombre_pasajero):
    pasajero_win = Tk()
    pasajero_win.title(f"Panel de Pasajero: {nombre_pasajero}")
    pasajero_win.geometry("800x700")

    Label(pasajero_win, text=f"BIENVENIDO PASAJERO: {nombre_pasajero}", font=("Arial", 14, "bold")).pack(pady=20)

    # Frame principal con pestañas simuladas
    notebook = Frame(pasajero_win)
    notebook.pack(pady=10, fill="both", expand=True)
    
    # Botones para diferentes funcionalidades
    frame_botones = Frame(notebook)
    frame_botones.pack(pady=10)
    
    Button(frame_botones, text="Buscar y Seleccionar Ruta", 
           command=lambda: ventana_seleccion_ruta(nombre_pasajero), width=30, height=2).grid(row=0, column=0, padx=10, pady=10)
    Button(frame_botones, text="Ver Mis Tickets", 
           command=lambda: ver_tickets_pasajero(nombre_pasajero), width=30, height=2).grid(row=0, column=1, padx=10, pady=10)
    Button(frame_botones, text="Historial de Compras (Recursivo)", 
           command=lambda: mostrar_historial_recursivo(nombre_pasajero, 0), width=30, height=2).grid(row=1, column=0, padx=10, pady=10)
    Button(frame_botones, text="Salir", 
           command=pasajero_win.destroy, width=30, height=2).grid(row=1, column=1, padx=10, pady=10)
    
    # Mostrar buses disponibles
    Label(notebook, text="BUSES DISPONIBLES:", font=("Arial", 12, "bold")).pack(pady=10)
    
    frame_buses = Frame(notebook)
    frame_buses.pack(pady=10, fill="both", expand=True)
    
    scrollbar = Scrollbar(frame_buses)
    scrollbar.pack(side="right", fill="y")
    
    lista_buses = Listbox(frame_buses, yscrollcommand=scrollbar.set, width=80, height=15)
    
    for bus in buses:
        disponibles = contar_asientos_disponibles(bus['asientos'])
        if disponibles > 0:
            lista_buses.insert("end", 
                f"Bus {bus['id']} | Cooperativa: {bus['cooperativa']} | Ruta: {bus['ruta']} | "
                f"Salida: {bus['hora_salida']} | Precio: ${bus['precio_base']:.2f} | "
                f"Asientos libres: {disponibles}/40")
    
    lista_buses.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=lista_buses.yview)
    
    # Botón para comprar en bus seleccionado
    def comprar_en_seleccionado():
        seleccion = lista_buses.curselection()
        if seleccion:
            texto = lista_buses.get(seleccion[0])
            bus_id = int(texto.split("Bus ")[1].split(" ")[0])
            ventana_seleccion_asiento(bus_id, nombre_pasajero)
        else:
            messagebox.showwarning("Selección", "Seleccione un bus de la lista")
    
    Button(notebook, text="Seleccionar este Bus y Elegir Asiento", 
           command=comprar_en_seleccionado, width=40).pack(pady=10)
    
    pasajero_win.mainloop()

def ventana_seleccion_ruta(nombre_pasajero):
    ventana = Toplevel()
    ventana.title("Búsqueda de Rutas")
    ventana.geometry("600x500")
    
    Label(ventana, text="BÚSQUEDA AVANZADA DE RUTAS", font=("Arial", 14, "bold")).pack(pady=10)
    
    frame_busqueda = Frame(ventana)
    frame_busqueda.pack(pady=10)
    
    Label(frame_busqueda, text="Origen:").grid(row=0, column=0, pady=5)
    entry_origen = Entry(frame_busqueda)
    entry_origen.grid(row=0, column=1, pady=5, padx=5)
    
    Label(frame_busqueda, text="Destino:").grid(row=1, column=0, pady=5)
    entry_destino = Entry(frame_busqueda)
    entry_destino.grid(row=1, column=1, pady=5, padx=5)
    
    def buscar():
        origen = entry_origen.get().strip()
        destino = entry_destino.get().strip()
        
        if not origen or not destino:
            messagebox.showwarning("Error", "Ingrese origen y destino")
            return
        
        # Usar función recursiva para búsqueda
        rutas_encontradas = buscar_rutas_recursivo(origen, destino, [], 0, 5)
        
        texto_resultados.delete(1.0, "end")
        
        if not rutas_encontradas:
            texto_resultados.insert("end", "No se encontraron rutas.\n")
            return
        
        texto_resultados.insert("end", f"Se encontraron {len(rutas_encontradas)} rutas posibles:\n\n")
        
        for i, ruta in enumerate(rutas_encontradas, 1):
            # Calcular precio recursivamente
            precio = calcular_precio_recursivo(ruta)
            
            texto_resultados.insert("end", f"RUTA {i}:\n")
            texto_resultados.insert("end", f"  Recorrido: {' -> '.join(ruta)}\n")
            texto_resultados.insert("end", f"  Precio estimado: ${precio:.2f}\n")
            
            # Buscar buses que coincidan con esta ruta
            buses_ruta = []
            for bus in buses:
                if origen in bus['ruta'] and destino in bus['ruta']:
                    buses_ruta.append(bus)
            
            if buses_ruta:
                texto_resultados.insert("end", f"  Buses disponibles: {len(buses_ruta)}\n")
                for bus in buses_ruta[:2]:  # Mostrar solo 2
                    texto_resultados.insert("end", f"    - Bus {bus['id']}: {bus['cooperativa']} a las {bus['hora_salida']} (${bus['precio_base']})\n")
            else:
                texto_resultados.insert("end", "  No hay buses directos para esta ruta\n")
            
            texto_resultados.insert("end", "\n")
    
    Button(frame_busqueda, text="Buscar Rutas", command=buscar).grid(row=2, column=0, columnspan=2, pady=10)
    
    # Resultados
    Label(ventana, text="Resultados:").pack(pady=5)
    
    frame_resultados = Frame(ventana)
    frame_resultados.pack(pady=10, fill="both", expand=True)
    
    scrollbar = Scrollbar(frame_resultados)
    scrollbar.pack(side="right", fill="y")
    
    texto_resultados = Text(frame_resultados, yscrollcommand=scrollbar.set, width=70, height=15)
    texto_resultados.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=texto_resultados.yview)
    
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

def ventana_seleccion_asiento(bus_id, nombre_pasajero):
    ventana = Toplevel()
    ventana.title(f"Selección de Asiento - Bus {bus_id}")
    ventana.geometry("600x700")
    
    # Buscar bus
    bus = next((b for b in buses if b['id'] == bus_id), None)
    if not bus:
        messagebox.showerror("Error", "Bus no encontrado")
        ventana.destroy()
        return
    
    Label(ventana, text=f"SELECCIÓN DE ASIENTO - Bus {bus_id}", font=("Arial", 14, "bold")).pack(pady=10)
    Label(ventana, text=f"Ruta: {bus['ruta']} | Salida: {bus['hora_salida']} | Precio: ${bus['precio_base']:.2f}").pack()
    
    # Canvas para matriz de asientos interactiva
    canvas = Canvas(ventana, width=500, height=400, bg="white")
    canvas.pack(pady=10)
    
    matriz = bus['asientos']
    filas = len(matriz)
    columnas = len(matriz[0])
    
    cell_size = 40
    start_x = 50
    start_y = 50
    
    # Dibujar matriz interactiva
    asientos_widgets = []
    
    for fila in range(filas):
        fila_widgets = []
        for col in range(columnas):
            x1 = start_x + col * cell_size
            y1 = start_y + fila * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            if matriz[fila][col] == 'L':  # Libre
                color = "green"
                estado = "Libre"
            else:  # Reservado
                color = "red"
                estado = "Ocupado"
            
            rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            texto = canvas.create_text((x1+x2)//2, (y1+y2)//2, text=f"{fila+1},{col+1}")
            
            # Guardar información del asiento
            info = {
                'rect': rect,
                'texto': texto,
                'fila': fila,
                'col': col,
                'estado': estado,
                'color': color
            }
            fila_widgets.append(info)
        asientos_widgets.append(fila_widgets)
    
    # Dibujar números de filas y columnas
    for col in range(columnas):
        x = start_x + col * cell_size + cell_size//2
        canvas.create_text(x, start_y - 20, text=str(col+1))
    
    for fila in range(filas):
        canvas.create_text(start_x - 20, start_y + fila * cell_size + cell_size//2, text=str(fila+1))
    
    # Información de selección
    Label(ventana, text="Haz clic en un asiento verde para seleccionarlo").pack(pady=5)
    
    seleccion_var = StringVar(ventana, value="Ningún asiento seleccionado")
    Label(ventana, textvariable=seleccion_var, font=("Arial", 10, "bold")).pack()
    
    # Variable para guardar asiento seleccionado
    asiento_seleccionado = {'fila': -1, 'col': -1}
    
    def on_canvas_click(event):
        nonlocal asiento_seleccionado
        
        # Calcular en qué celda se hizo clic
        col = (event.x - start_x) // cell_size
        fila = (event.y - start_y) // cell_size
        
        if 0 <= fila < filas and 0 <= col < columnas:
            asiento = asientos_widgets[fila][col]
            
            if asiento['estado'] == 'Libre':
                # Resetear color de selección anterior
                if asiento_seleccionado['fila'] != -1:
                    prev = asientos_widgets[asiento_seleccionado['fila']][asiento_seleccionado['col']]
                    canvas.itemconfig(prev['rect'], fill='green')
                
                # Resaltar nuevo selección
                canvas.itemconfig(asiento['rect'], fill='blue')
                asiento_seleccionado = {'fila': fila, 'col': col}
                seleccion_var.set(f"Asiento seleccionado: Fila {fila+1}, Columna {col+1}")
            else:
                messagebox.showwarning("Asiento Ocupado", "Este asiento ya está reservado")
    
    canvas.bind("<Button-1>", on_canvas_click)
    
    # Botón de compra
    def comprar_boleto():
        if asiento_seleccionado['fila'] == -1:
            messagebox.showwarning("Selección", "Seleccione un asiento primero")
            return
        
        fila = asiento_seleccionado['fila']
        col = asiento_seleccionado['col']
        
        # Confirmar compra
        respuesta = messagebox.askyesno(
            "Confirmar Compra",
            f"¿Desea comprar el asiento Fila {fila+1}, Columna {col+1}?\n"
            f"Bus: {bus['ruta']}\n"
            f"Precio: ${bus['precio_base']:.2f}"
        )
        
        if respuesta:
            # Reservar asiento
            if reservar_asiento(bus['asientos'], fila, col):
                # Crear ticket
                nuevo_ticket = {
                    "id": len(tickets) + 1,
                    "pasajero": nombre_pasajero,
                    "bus_id": bus_id,
                    "ruta": bus['ruta'],
                    "hora_salida": bus['hora_salida'],
                    "asiento_fila": fila + 1,
                    "asiento_columna": col + 1,
                    "precio": bus['precio_base'],
                    "fecha_compra": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                tickets.append(nuevo_ticket)
                guardar_datos()
                
                # Agregar al historial (para recursividad)
                historial_compras.append({
                    "pasajero": nombre_pasajero,
                    "accion": f"Compra ticket #{nuevo_ticket['id']}",
                    "fecha": nuevo_ticket['fecha_compra']
                })
                
                messagebox.showinfo("Éxito", 
                    f"¡Compra exitosa!\n"
                    f"Ticket #{nuevo_ticket['id']}\n"
                    f"Asiento: {fila+1}-{col+1}\n"
                    f"Precio: ${bus['precio_base']:.2f}")
                
                # Actualizar vista
                ventana.destroy()
                # Volver a abrir ventana de pasajero
                ventana_pasajero(nombre_pasajero)
            else:
                messagebox.showerror("Error", "El asiento ya fue reservado")
    
    Button(ventana, text="Comprar Boleto", command=comprar_boleto, width=20, height=2).pack(pady=10)
    Button(ventana, text="Cancelar", command=ventana.destroy).pack(pady=5)

def ver_tickets_pasajero(nombre_pasajero):
    ventana = Toplevel()
    ventana.title("Mis Tickets")
    
    tickets_pasajero = [t for t in tickets if t['pasajero'] == nombre_pasajero]
    
    if not tickets_pasajero:
        Label(ventana, text="No tienes tickets comprados.").pack(pady=20)
    else:
        Label(ventana, text=f"MIS TICKETS ({len(tickets_pasajero)})", font=("Arial", 14, "bold")).pack(pady=10)
        
        frame = Frame(ventana)
        frame.pack(pady=10, fill="both", expand=True)
        
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        
        texto = Text(frame, yscrollcommand=scrollbar.set, width=70, height=20)
        texto.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=texto.yview)
        
        for ticket in tickets_pasajero:
            texto.insert("end", f"Ticket #{ticket['id']}\n")
            texto.insert("end", f"  Ruta: {ticket['ruta']}\n")
            texto.insert("end", f"  Hora salida: {ticket['hora_salida']}\n")
            texto.insert("end", f"  Asiento: Fila {ticket['asiento_fila']}, Columna {ticket['asiento_columna']}\n")
            texto.insert("end", f"  Precio: ${ticket['precio']:.2f}\n")
            texto.insert("end", f"  Fecha compra: {ticket['fecha_compra']}\n")
            texto.insert("end", "-" * 50 + "\n")
    
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

def mostrar_historial_recursivo(nombre_pasajero, nivel=0):
    """Función recursiva para mostrar historial con sangría"""
    ventana = Toplevel()
    ventana.title("Historial de Compras (Recursivo)")
    
    texto = Text(ventana, width=70, height=25)
    texto.pack(pady=10)
    
    texto.insert("end", f"HISTORIAL RECURSIVO PARA: {nombre_pasajero}\n\n")
    
    # Filtrar historial del pasajero
    historial_pasajero = [h for h in historial_compras if nombre_pasajero in h['pasajero']]
    
    def imprimir_recursivo(historial, indice, nivel):
        if indice >= len(historial):
            return
        
        item = historial[indice]
        sangria = "  " * nivel
        texto.insert("end", f"{sangria}Nivel {nivel}: {item['accion']} - {item['fecha']}\n")
        
        # Llamada recursiva para el siguiente item
        imprimir_recursivo(historial, indice + 1, nivel + 1)
    
    if historial_pasajero:
        imprimir_recursivo(historial_pasajero, 0, 0)
        
        # También mostrar tickets del pasajero de forma recursiva
        texto.insert("end", "\n\nTICKETS COMPRADOS (Recursivo):\n")
        tickets_pasajero = [t for t in tickets if t['pasajero'] == nombre_pasajero]
        
        def mostrar_tickets_recursivo(tickets_list, indice):
            if indice >= len(tickets_list):
                return
            
            ticket = tickets_list[indice]
            texto.insert("end", f"  Ticket {indice+1}: #{ticket['id']} - {ticket['ruta']}\n")
            mostrar_tickets_recursivo(tickets_list, indice + 1)
        
        mostrar_tickets_recursivo(tickets_pasajero, 0)
    else:
        texto.insert("end", "No hay historial de compras.\n")
    
    texto.insert("end", f"\nTotal de acciones en historial: {len(historial_pasajero)}")
    
    Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

# VENTANA PRINCIPAL DE LOGIN (MODIFICADA) ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
def ventana_login():
    root = Tk()
    root.title("Sistema de Transporte - Login")
    root.geometry("500x500")

    # Cargar datos al iniciar
    crear_directorios()
    cargar_datos()
    
    # Crear admin por defecto si no existe
    if not any(u["tipo"] == "admin" for u in usuarios):
        usuarios.append({
            "usuario": "admin",
            "contraseña": "admin123",
            "tipo": "admin"
        })
        guardar_datos()

    frame_superior = Frame(root)
    frame_superior.pack(fill="both", expand=True)
    frame_inferior = Frame(root)
    frame_inferior.pack(fill="both", expand=True)
    
    # Título
    Label(frame_superior, text="SISTEMA DE TRANSPORTE", font=("Arial", 16, "bold")).pack(pady=20)
    Label(frame_superior, text="Login", font=("Arial", 14)).pack(pady=10)
    
    # Logo (si existe)
    try:
        img = Image.open("imagenes/logo.png")
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        render = ImageTk.PhotoImage(img)
        lbl_img = Label(frame_superior, image=render)
        lbl_img.image = render
        lbl_img.pack(pady=10)
    except:
        pass  # Si no hay logo, continuar sin él

    # Campos de entrada
    frame_campos = Frame(frame_inferior)
    frame_campos.pack(pady=20)
    
    Label(frame_campos, text="Usuario:", font=("Arial", 10)).grid(row=0, column=0, pady=5, sticky="e")
    entry_user = Entry(frame_campos, width=25)
    entry_user.grid(row=0, column=1, pady=5, padx=10)
    
    Label(frame_campos, text="Contraseña:", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="e")
    entry_contra = Entry(frame_campos, show="*", width=25)
    entry_contra.grid(row=1, column=1, pady=5, padx=10)

    # Botones
    frame_botones = Frame(frame_inferior)
    frame_botones.pack(pady=20)
    
    Button(frame_botones, text="Ingresar",
           command=lambda: entrar(entry_user, entry_contra, root),
           width=15, height=2).pack(side="left", padx=10)
    
    Button(frame_botones, text="Registrar",
           command=lambda: abrir_registro(root),
           width=15, height=2).pack(side="left", padx=10)
    
    # Información del sistema
    Label(frame_inferior, 
          text=f"Sistema cargado: {len(usuarios)} usuarios, {len(rutas)} rutas, {len(buses)} buses",
          font=("Arial", 8)).pack(pady=10)
    
    root.mainloop()

# INICIO DEL PROGRAMA ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦
ventana_login()
ventana_login()
