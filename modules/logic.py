# --- GRAFOS (DIJKSTRA & BÚSQUEDA) ---

def dijkstra(origen, destino, grafo):
    if origen not in grafo or destino not in grafo:
        return None, float('inf')
    
    distancias = {ciudad: float('inf') for ciudad in grafo}
    distancias[origen] = 0
    previos = {ciudad: None for ciudad in grafo}
    visitados = set()
    
    while len(visitados) < len(distancias):
        ciudad_actual = None
        min_distancia = float('inf')
        
        for ciudad in grafo:
            if ciudad not in visitados and distancias[ciudad] < min_distancia:
                min_distancia = distancias[ciudad]
                ciudad_actual = ciudad
        
        if ciudad_actual is None or ciudad_actual == destino:
            break
        
        visitados.add(ciudad_actual)
        
        for vecino, costo in grafo[ciudad_actual]:
            nueva_distancia = distancias[ciudad_actual] + costo
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                previos[vecino] = ciudad_actual
    
    ruta = []
    actual = destino
    while actual is not None:
        ruta.insert(0, actual)
        actual = previos[actual]
    
    if ruta[0] != origen:
        return None, float('inf')
    
    return ruta, distancias[destino]

def buscar_todas_rutas(origen, destino, grafo, visitados=None, ruta_actual=None):
    if visitados is None: visitados = set()
    if ruta_actual is None: ruta_actual = []
    
    visitados.add(origen)
    ruta_actual.append(origen)
    
    rutas_encontradas = []
    
    if origen == destino:
        rutas_encontradas.append(list(ruta_actual))
    else:
        for vecino, _ in grafo.get(origen, []):
            if vecino not in visitados:
                rutas_recursivas = buscar_todas_rutas(vecino, destino, grafo, visitados.copy(), list(ruta_actual))
                rutas_encontradas.extend(rutas_recursivas)
    
    return rutas_encontradas

def rutas_mas_economica_cara(origen, destino, grafo):
    todas_rutas = buscar_todas_rutas(origen, destino, grafo)
    
    if not todas_rutas:
        return None, None, 0, 0
    
    mejor_ruta = None
    peor_ruta = None
    menor_costo = float('inf')
    mayor_costo = 0
    
    for ruta in todas_rutas:
        costo_total = 0
        for i in range(len(ruta) - 1):
            for vecino, costo in grafo[ruta[i]]:
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

# --- MATRICES (ASIENTOS) ---

def crear_matriz_asientos(filas=10, columnas=4):
    return [['L' for _ in range(columnas)] for _ in range(filas)]

def contar_asientos_disponibles(matriz):
    disponibles = 0
    for fila in matriz:
        for asiento in fila:
            if asiento == 'L':
                disponibles += 1
    return disponibles

def reservar_asiento(matriz, fila, columna):
    if 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0]):
        if matriz[fila][columna] == 'L':
            matriz[fila][columna] = 'R'
            return True
    return False

def mostrar_matriz_asientos(matriz):
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

# --- RECURSIVIDAD ---

def buscar_rutas_recursivo(ciudad_actual, destino, grafo, visitadas, profundidad, max_profundidad=3):
    if profundidad > max_profundidad:
        return []
    
    if ciudad_actual == destino:
        return [[ciudad_actual]]
    
    visitadas.append(ciudad_actual)
    rutas = []
    
    for vecino, _ in grafo.get(ciudad_actual, []):
        if vecino not in visitadas:
            rutas_parciales = buscar_rutas_recursivo(vecino, destino, grafo, visitadas.copy(), profundidad + 1, max_profundidad)
            for ruta in rutas_parciales:
                rutas.append([ciudad_actual] + ruta)
    
    return rutas

def calcular_precio_recursivo(ruta, grafo, indice=0):
    if indice >= len(ruta) - 1:
        return 0
    
    ciudad_actual = ruta[indice]
    siguiente = ruta[indice + 1]
    
    for vecino, costo in grafo.get(ciudad_actual, []):
        if vecino == siguiente:
            return costo + calcular_precio_recursivo(ruta, grafo, indice + 1)
    
    return 0