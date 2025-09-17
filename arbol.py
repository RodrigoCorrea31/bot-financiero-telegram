import requests

class NodoArbol:
    def __init__(self, moneda, tasa):
        self.moneda = moneda  
        self.tasa = tasa      
        self.izquierda = None 
        self.derecha = None   

class ArbolBinario:
    def __init__(self):
        self.raiz = None 

    def insertar(self, moneda, tasa):
        nuevo_nodo = NodoArbol(moneda, tasa)
        if self.raiz is None:
            self.raiz = nuevo_nodo  
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo)

    def _insertar_recursivo(self, actual, nuevo_nodo):
        if nuevo_nodo.moneda < actual.moneda:
            if actual.izquierda is None:
                actual.izquierda = nuevo_nodo
            else:
                self._insertar_recursivo(actual.izquierda, nuevo_nodo)
        else:
            if actual.derecha is None:
                actual.derecha = nuevo_nodo
            else:
                self._insertar_recursivo(actual.derecha, nuevo_nodo)

    def recorrido_inorden(self):
        resultado = []
        self._recorrido_inorden(self.raiz, resultado)
        return resultado

    def _recorrido_inorden(self, nodo, resultado):
        if nodo:
            self._recorrido_inorden(nodo.izquierda, resultado)
            resultado.append((nodo.moneda, nodo.tasa))
            self._recorrido_inorden(nodo.derecha, resultado)

    def recorrido_preorden(self):
        resultado = []
        self._recorrido_preorden(self.raiz, resultado)
        return resultado

    def _recorrido_preorden(self, nodo, resultado):
        if nodo:
            resultado.append((nodo.moneda, nodo.tasa))
            self._recorrido_preorden(nodo.izquierda, resultado)
            self._recorrido_preorden(nodo.derecha, resultado)

    def recorrido_postorden(self):
        resultado = []
        self._recorrido_postorden(self.raiz, resultado)
        return resultado

    def _recorrido_postorden(self, nodo, resultado):
        if nodo:
            self._recorrido_postorden(nodo.izquierda, resultado)
            self._recorrido_postorden(nodo.derecha, resultado)
            resultado.append((nodo.moneda, nodo.tasa))

def obtener_tasas_cambio():
    url = "https://api.frankfurter.app/latest?base=USD"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos["rates"]
    else:
        raise Exception("Error al conectar con la API de Frankfurter")

def construir_arbol_monedas():
    tasas = obtener_tasas_cambio()  
    arbol = ArbolBinario()        

    arbol.insertar("USD", 1.0)

    for moneda, tasa in tasas.items():
        arbol.insertar(moneda, tasa)

    return arbol

def obtener_arbol_monedas():
    return construir_arbol_monedas() 

def selection_sort(data):
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j][0] < data[min_idx][0]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data

def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key[0] < data[j][0]:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j][0] > data[j + 1][0]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

def merge_sort(data):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]
        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][0] < right_half[j][0]:
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1
    return data

def quick_sort(data):
    if len(data) <= 1:
        return data
    pivot = data[0]
    less = [item for item in data[1:] if item[0] <= pivot[0]]
    greater = [item for item in data[1:] if item[0] > pivot[0]]
    return quick_sort(less) + [pivot] + quick_sort(greater)



def arbol_a_lista(nodo, lista=None):
    if lista is None:
        lista = []
    if nodo is not None:
        lista.append((nodo.nombre, nodo.tasa))
        arbol_a_lista(nodo.izquierda, lista)
        arbol_a_lista(nodo.derecha, lista)
    return lista

def buscar_moneda(lista, nombre, index=0):
    if index >= len(lista):
        return None  
    if lista[index][0].lower() == nombre.lower(): 
        return lista[index]
    return buscar_moneda(lista, nombre, index + 1)

def arbol_a_lista(arbol):
    """
    Convierte el árbol binario en una lista de tuplas (moneda, tasa).
    """
    resultado = []
    _arbol_a_lista_recursivo(arbol.raiz, resultado)
    return resultado

def _arbol_a_lista_recursivo(nodo, resultado):
    """
    Recorrido inorden recursivo para convertir un árbol binario a lista.
    """
    if nodo:
        _arbol_a_lista_recursivo(nodo.izquierda, resultado)
        resultado.append((nodo.moneda, nodo.tasa))
        _arbol_a_lista_recursivo(nodo.derecha, resultado)


def buscar_moneda(lista, nombre, index=0):
    """
    Busca una moneda en una lista de forma recursiva.
    
    Parámetros:
    - lista: Lista de tuplas (moneda, tasa).
    - nombre: Nombre o símbolo de la moneda a buscar.
    - index: Índice actual para la búsqueda recursiva.
    
    Retorna:
    - Tupla (moneda, tasa) si se encuentra, o None si no se encuentra.
    """
    if index >= len(lista):
        return None 
    if lista[index][0].lower() == nombre.lower():  
        return lista[index]
    return buscar_moneda(lista, nombre, index + 1)
