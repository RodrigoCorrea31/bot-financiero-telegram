import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from arbol import construir_arbol_monedas, arbol_a_lista, buscar_moneda, selection_sort, insertion_sort, bubble_sort, merge_sort, quick_sort, obtener_arbol_monedas
from transacciones import GrafoTransacciones, realizar_transaccion, mostrar_ganancias, obtener_variacion_temporal

API_TOKEN = '7873438414:AAFTX6OFUPMYHB6bpDFQ-DipHs9Iq-DNyNw'

bot = telebot.TeleBot(API_TOKEN)

arbol = construir_arbol_monedas()
grafo_transacciones = GrafoTransacciones()
transacciones_temporales = {}

@bot.message_handler(commands=['start', 'menu'])
def mostrar_menu_principal(message):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("1️⃣ Operaciones con el árbol binario")
    btn2 = KeyboardButton("2️⃣ Ordenación de monedas")
    btn3 = KeyboardButton("3️⃣ Buscar moneda")
    btn4 = KeyboardButton("4️⃣ Realizar transacción")
    btn5 = KeyboardButton("5️⃣ Ver ganancias")
    btn6 = KeyboardButton("6️⃣ Análisis de variación temporal")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(
        message.chat.id,
        "Bienvenido al Bot Financiero. Seleccione una opción:\n\n"
        "1️⃣ Operaciones con el árbol binario\n"
        "2️⃣ Ordenación de monedas\n"
        "3️⃣ Buscar moneda\n"
        "4️⃣ Realizar transacción\n"
        "5️⃣ Ver ganancias\n"
        "6️⃣ Análisis de variación temporal\n",
        reply_markup=markup,
    )

def mostrar_submenu_arbol(message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = KeyboardButton("🔹 Preorden")
    btn2 = KeyboardButton("🔹 Inorden")
    btn3 = KeyboardButton("🔹 Postorden")
    btn_back = KeyboardButton("🔙 Volver al menú principal")
    markup.add(btn1, btn2, btn3, btn_back)

    bot.send_message(
        message.chat.id,
        "Seleccione una operación con el árbol binario:\n\n"
        "🔹 Preorden\n"
        "🔹 Inorden\n"
        "🔹 Postorden\n",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text in ["🔹 Preorden", "🔹 Inorden", "🔹 Postorden"])
def manejar_recorridos_arbol(message):
    if message.text == "🔹 Preorden":
        recorrido = arbol.recorrido_preorden()
    elif message.text == "🔹 Inorden":
        recorrido = arbol.recorrido_inorden()
    elif message.text == "🔹 Postorden":
        recorrido = arbol.recorrido_postorden()

    resultado = "\n".join([f"{moneda}: {tasa}" for moneda, tasa in recorrido])
    bot.send_message(
        message.chat.id,
        f"Recorrido {message.text.split(' ')[1]}:\n\n{resultado}"
    )

@bot.message_handler(func=lambda message: message.text == "🔙 Volver al menú principal")
def volver_al_menu_principal(message):
    mostrar_menu_principal(message)

def mostrar_submenu_ordenacion(message):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("🔸 Selection Sort")
    btn2 = KeyboardButton("🔸 Insert Sort")
    btn3 = KeyboardButton("🔸 Bubble Sort")
    btn4 = KeyboardButton("🔸 Merge Sort")
    btn5 = KeyboardButton("🔸 Quick Sort")
    btn_back = KeyboardButton("🔙 Volver al menú principal")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn_back)

    bot.send_message(
        message.chat.id,
        "Seleccione un algoritmo de ordenación:\n\n"
        "🔸 Selection Sort\n"
        "🔸 Insert Sort\n"
        "🔸 Bubble Sort\n"
        "🔸 Merge Sort\n"
        "🔸 Quick Sort\n",
        reply_markup=markup,
    )

@bot.message_handler(func=lambda message: message.text in [
    "🔸 Selection Sort", "🔸 Insert Sort", "🔸 Bubble Sort", "🔸 Merge Sort", "🔸 Quick Sort"
])
def manejar_ordenacion(message):
    monedas = arbol.recorrido_inorden() 
    algoritmo = message.text.split(" ")[1]

    if algoritmo == "Selection":
        ordenado = selection_sort(monedas)
    elif algoritmo == "Insert":
        ordenado = insertion_sort(monedas)
    elif algoritmo == "Bubble":
        ordenado = bubble_sort(monedas)
    elif algoritmo == "Merge":
        ordenado = merge_sort(monedas)
    elif algoritmo == "Quick":
        ordenado = quick_sort(monedas)

    resultado = "\n".join([f"{moneda}: {tasa}" for moneda, tasa in ordenado])
    bot.send_message(
        message.chat.id,
        f"Monedas ordenadas en base a {algoritmo} Sort:\n\n{resultado}"
    )

@bot.message_handler(func=lambda message: message.text == "3️⃣ Buscar moneda")
def buscar_moneda_handler(message):
    msg = bot.reply_to(message, "Ingrese el nombre o símbolo de la moneda que desea buscar:")
    bot.register_next_step_handler(msg, realizar_busqueda)

def realizar_busqueda(message):
    nombre_moneda = message.text.strip()
    lista_monedas = arbol_a_lista(arbol) 
    resultado = buscar_moneda(lista_monedas, nombre_moneda)

    if resultado:
        moneda, tasa = resultado
        bot.send_message(
            message.chat.id,
            f"Moneda encontrada:\n\nNombre: {moneda}\nTasa de cambio: {tasa}"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Lo siento, no se encontró ninguna moneda con ese nombre o símbolo."
        )

@bot.message_handler(func=lambda message: message.text == "4️⃣ Realizar transacción")
def iniciar_transaccion(message):
    transacciones_temporales[message.chat.id] = {} 
    msg = bot.reply_to(message, "Ingrese la moneda de origen:")
    bot.register_next_step_handler(msg, obtener_moneda_destino)

def obtener_moneda_destino(message):
    transacciones_temporales[message.chat.id]['moneda_origen'] = message.text.strip().upper()
    msg = bot.reply_to(message, "Ingrese la moneda de destino:")
    bot.register_next_step_handler(msg, obtener_monto_transaccion)

def obtener_monto_transaccion(message):
    transacciones_temporales[message.chat.id]['moneda_destino'] = message.text.strip().upper()
    msg = bot.reply_to(message, "Ingrese el monto de la moneda de origen:")
    bot.register_next_step_handler(msg, confirmar_transaccion)

def confirmar_transaccion(message):
    try:
        monto_origen = float(message.text.strip())
        transaccion = transacciones_temporales[message.chat.id]
        transaccion['monto_origen'] = monto_origen

        moneda_origen = transaccion["moneda_origen"]
        moneda_destino = transaccion["moneda_destino"]

        resultado_previo = realizar_transaccion(
            arbol, grafo_transacciones, moneda_origen, moneda_destino, monto_origen, calcular_sin_guardar=True
        )

        if "error" in resultado_previo:
            bot.send_message(message.chat.id, resultado_previo["error"])
            return

        bot.send_message(
            message.chat.id,
            f"Usted recibirá: {resultado_previo['monto_destino']:.2f} {moneda_destino}.\n"
            f"Comisión aplicada: {resultado_previo['comision']:.2f} {moneda_origen}.\n\n"
            "¿Desea confirmar esta transacción? Responda 'Sí' o 'No'."
        )

        bot.register_next_step_handler(message, finalizar_transaccion)
    except ValueError:
        bot.send_message(message.chat.id, "Por favor ingrese un monto válido.")

def finalizar_transaccion(message):
    if message.text.strip().lower() == 'sí':
        transaccion = transacciones_temporales[message.chat.id]
        moneda_origen = transaccion["moneda_origen"]
        moneda_destino = transaccion["moneda_destino"]
        monto_origen = transaccion["monto_origen"]

        resultado = realizar_transaccion(arbol, grafo_transacciones, moneda_origen, moneda_destino, monto_origen)

        if "mensaje" in resultado:
            bot.send_message(message.chat.id, resultado["mensaje"])
        else:
            bot.send_message(message.chat.id, "Hubo un error en la transacción.")
    else:
        bot.send_message(message.chat.id, "Transacción cancelada.")

    transacciones_temporales.pop(message.chat.id, None)


@bot.message_handler(func=lambda message: message.text == "5️⃣ Ver ganancias")
def mostrar_ganancias_handler(message):
    ganancias = mostrar_ganancias(grafo_transacciones, arbol)
    bot.send_message(message.chat.id, ganancias)

@bot.message_handler(commands=['variacion'])
def manejar_variacion(message):
    arbol_monedas = obtener_arbol_monedas() 

    bot.reply_to(message, "Ingrese la fecha de inicio (formato YYYY-MM-DD):")
    bot.register_next_step_handler(message, obtener_fecha_inicio, arbol_monedas)

def obtener_fecha_inicio(message, arbol_monedas):
    fecha_inicio = message.text.strip()
    bot.reply_to(message, "Ingrese la fecha de fin (formato YYYY-MM-DD):")
    bot.register_next_step_handler(message, obtener_fecha_fin, fecha_inicio, arbol_monedas)

def obtener_fecha_fin(message, fecha_inicio, arbol_monedas):
    fecha_fin = message.text.strip()
    bot.reply_to(message, "Ingrese el símbolo de la moneda de referencia (ejemplo: EUR, JPY):")
    bot.register_next_step_handler(message, calcular_variacion, fecha_inicio, fecha_fin, arbol_monedas)

def calcular_variacion(message, fecha_inicio, fecha_fin, arbol_monedas):
    moneda_referencia = message.text.strip()
    respuesta = obtener_variacion_temporal(arbol_monedas, fecha_inicio, fecha_fin, moneda_referencia)
    bot.reply_to(message, respuesta)

@bot.message_handler(func=lambda message: message.text in [
    "1️⃣ Operaciones con el árbol binario",
    "2️⃣ Ordenación de monedas",
    "3️⃣ Buscar moneda",
    "4️⃣ Realizar transacción",
    "5️⃣ Ver ganancias",
    "6️⃣ Análisis de variación temporal"
])
def manejar_opcion(message):
    if message.text == "1️⃣ Operaciones con el árbol binario":
        mostrar_submenu_arbol(message)
    elif message.text == "2️⃣ Ordenación de monedas":
        mostrar_submenu_ordenacion(message)
    elif message.text == "3️⃣ Buscar moneda":
        buscar_moneda_handler(message)
    elif message.text == "4️⃣ Realizar transacción":
        iniciar_transaccion(message)
    elif message.text == "5️⃣ Ver ganancias":
        mostrar_ganancias_handler(message)
    elif message.text == "6️⃣ Análisis de variación temporal":
        manejar_variacion(message)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    Comandos disponibles:
    /start - Iniciar el bot
    /help - Mostrar este mensaje
    Más funcionalidades se agregarán próximamente.
    """
    bot.reply_to(message, help_text)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, "Opción no válida. Por favor seleccione una opción del menú principal.")

if __name__ == "__main__":
    print("Bot iniciado...")
    bot.infinity_polling()
