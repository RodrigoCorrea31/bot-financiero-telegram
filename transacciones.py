from arbol import arbol_a_lista
import requests
from datetime import datetime

class GrafoTransacciones:
    def __init__(self):
        self.transacciones = {}

    def agregar_transaccion(self, moneda_origen, moneda_destino, monto_comision):
        """
        Agregar una transacción al grafo. Solo se almacena la comisión como ganancia acumulada.
        """
        if moneda_origen not in self.transacciones:
            self.transacciones[moneda_origen] = {}
        if moneda_destino not in self.transacciones[moneda_origen]:
            self.transacciones[moneda_origen][moneda_destino] = 0
        self.transacciones[moneda_origen][moneda_destino] += monto_comision

    def obtener_ganancias(self):
        """
        Retorna el diccionario de transacciones que registra las ganancias acumuladas.
        """
        return self.transacciones


def realizar_transaccion(arbol, grafo, moneda_origen, moneda_destino, monto_origen, calcular_sin_guardar=False):
    """
    Realiza una transacción entre dos monedas, aplicando un 2% de comisión. Si calcular_sin_guardar es True,
    solo calcula el resultado sin registrar la transacción.
    """
    lista_monedas = arbol_a_lista(arbol)

    tasa_origen = next((tasa for moneda, tasa in lista_monedas if moneda == moneda_origen), None)
    tasa_destino = next((tasa for moneda, tasa in lista_monedas if moneda == moneda_destino), None)

    if tasa_origen is None:
        return {"error": f"No se encontró la moneda de origen: {moneda_origen}."}
    if tasa_destino is None:
        return {"error": f"No se encontró la moneda de destino: {moneda_destino}."}

    monto_con_comision = monto_origen * 0.98
    comision = monto_origen * 0.02

    monto_destino = (monto_con_comision / tasa_origen) * tasa_destino

    if calcular_sin_guardar:
        return {
            "monto_destino": monto_destino,
            "comision": comision
        }

    grafo.agregar_transaccion(moneda_origen, moneda_destino, comision)

    return {
        "monto_destino": monto_destino,
        "comision": comision,
        "mensaje": (f"Transacción confirmada.\n"
                    f"Monto en {moneda_origen}: {monto_origen:.2f}\n"
                    f"Monto en {moneda_destino}: {monto_destino:.2f}\n"
                    f"Comisión aplicada: {comision:.2f} {moneda_origen}.")
    }


def mostrar_ganancias(grafo, arbol):
    """
    Calcula las ganancias acumuladas en dólares recorriendo el grafo de transacciones.
    """
    lista_monedas = arbol_a_lista(arbol)
    ganancias_totales = 0

    for moneda_origen, destinos in grafo.obtener_ganancias().items():
        for moneda_destino, monto in destinos.items():
            tasa_origen = next((tasa for moneda, tasa in lista_monedas if moneda == moneda_origen), None)

            if tasa_origen:
                ganancias_totales += monto / tasa_origen 

    return f"Ganancias totales en USD: {ganancias_totales:.2f}."


def obtener_variacion_temporal(arbol, fecha_inicio, fecha_fin, moneda_referencia):
    """
    Calcula la variación temporal del valor de una moneda respecto al dólar en un rango de fechas.
    """
    api_url = "https://api.frankfurter.app/"
    lista_monedas = arbol_a_lista(arbol)

    try:
        datetime.strptime(fecha_inicio, "%Y-%m-%d")
        datetime.strptime(fecha_fin, "%Y-%m-%d")

        if not any(moneda == moneda_referencia for moneda, _ in lista_monedas):
            return f"La moneda {moneda_referencia} no se encuentra disponible en el árbol."

        response_inicio = requests.get(f"{api_url}{fecha_inicio}?from=USD")
        response_fin = requests.get(f"{api_url}{fecha_fin}?from=USD")

        if response_inicio.status_code != 200 or response_fin.status_code != 200:
            return "Error al obtener datos de la API de Frankfurter."

        datos_inicio = response_inicio.json().get("rates", {})
        datos_fin = response_fin.json().get("rates", {})

        if moneda_referencia not in datos_inicio or moneda_referencia not in datos_fin:
            return f"La moneda {moneda_referencia} no está disponible en el período indicado."

        tasa_inicio = datos_inicio[moneda_referencia]
        tasa_fin = datos_fin[moneda_referencia]

        variacion_porcentual = ((tasa_fin - tasa_inicio) / tasa_inicio) * 100

        return (
            f"Variación de la moneda {moneda_referencia} respecto al USD:\n"
            f"- Tasa inicial ({fecha_inicio}): {tasa_inicio}\n"
            f"- Tasa final ({fecha_fin}): {tasa_fin}\n"
            f"- Variación porcentual: {variacion_porcentual:.2f}%"
        )
    except ValueError:
        return "Formato de fecha inválido. Por favor, ingrese las fechas en formato YYYY-MM-DD."
    except Exception as e:
        return f"Error inesperado: {e}"
