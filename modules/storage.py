import json
import os

# ESTRUCTURAS DE DATOS GLOBALES
usuarios = []
cooperativas = []
rutas = []
buses = []
tickets = []
grafo_rutas = {}
historial_compras = []

# ARCHIVOS
DATA_DIR = "data"
ARCHIVO_USUARIOS = os.path.join(DATA_DIR, "usuarios.json")
ARCHIVO_COOPERATIVAS = os.path.join(DATA_DIR, "cooperativas.json")
ARCHIVO_RUTAS = os.path.join(DATA_DIR, "rutas.json")
ARCHIVO_BUSES = os.path.join(DATA_DIR, "buses.json")
ARCHIVO_TICKETS = os.path.join(DATA_DIR, "tickets.json")

def crear_directorios():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

def reconstruir_grafo():
    global grafo_rutas
    grafo_rutas.clear()
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

def cargar_datos():
    global usuarios, cooperativas, rutas, buses, tickets
    try:
        if os.path.exists(ARCHIVO_USUARIOS):
            with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as f:
                usuarios[:] = json.load(f)
        
        if os.path.exists(ARCHIVO_COOPERATIVAS):
            with open(ARCHIVO_COOPERATIVAS, 'r', encoding='utf-8') as f:
                cooperativas[:] = json.load(f)
        
        if os.path.exists(ARCHIVO_RUTAS):
            with open(ARCHIVO_RUTAS, 'r', encoding='utf-8') as f:
                rutas[:] = json.load(f)
                reconstruir_grafo()
        
        if os.path.exists(ARCHIVO_BUSES):
            with open(ARCHIVO_BUSES, 'r', encoding='utf-8') as f:
                buses[:] = json.load(f)
        
        if os.path.exists(ARCHIVO_TICKETS):
            with open(ARCHIVO_TICKETS, 'r', encoding='utf-8') as f:
                tickets[:] = json.load(f)
                
    except Exception as e:
        print(f"Error cargando datos: {e}")

def guardar_datos():
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