## Bot Financiero

Bot desarrollado para Telegram que permite realizar operaciones financieras y de cambio de divisas en tiempo real, utilizando estructuras de datos (árboles binarios, grafos y algoritmos de ordenación) y conectándose a la API de Frankfurter para obtener tasas actualizadas.

## Descripción general

El Bot Financiero ofrece una experiencia interactiva en Telegram para consultar y operar con distintas monedas.
Entre sus principales funciones se incluyen:

Consultar tasas de cambio en tiempo real.

Realizar transacciones cambiarias entre monedas.

Ordenar monedas mediante distintos algoritmos de ordenación (Selection Sort, Insert Sort, Bubble Sort, Merge Sort, Quick Sort).

Visualizar monedas en recorridos de árboles binarios (preorden, inorden, postorden).

Consultar ganancias acumuladas.

Analizar variaciones temporales del valor de las monedas.

## Tecnologías y conceptos aplicados

Lenguaje: Python

Estructuras de datos: Árbol binario, grafos

Algoritmos: Ordenación (Selection, Insert, Bubble, Merge, Quick Sort)

API Externa: Frankfurter API

Plataforma: Telegram Bot API

Librerías utilizadas:

requests (para conexión con la API)

telebot o python-telegram-bot (para la interacción con Telegram)

datetime, json, y collections para manejo de datos

## Funcionalidades principales
# Menú principal

Operaciones con árbol binario: Visualización en preorden, inorden y postorden.

Ordenación de monedas: Aplicación de diferentes algoritmos de ordenación.

Buscar moneda: Consulta por nombre o símbolo (ej: EUR, GBP).

Realizar transacción: Cambio de divisas con comisión del 2%.

Ver ganancias: Muestra el total de ganancias en USD.

Variación temporal: Análisis de variación porcentual de una moneda en un rango de fechas.

## Instalación y ejecución
1. Clonar el repositorio:
git clone https://github.com/RodrigoCorrea31/bot-financiero-telegram.git
cd ObligatorioBotAlgoritmos

## 2. Crear y activar un entorno virtual (recomendado)
En Windows:
python -m venv botObligatorio
botObligatorio\Scripts\activate

En Linux / macOS:
python3 -m venv botObligatorio
source botObligatorio/bin/activate

## 3. Instalar dependencias

Asegúrate de tener el archivo requirements.txt en la raíz.
Luego, ejecutá:

pip install -r requirements.txt

## 4. Configurar el bot

El bot utiliza la API de Frankfurter (no requiere autenticación).
Solo necesitás configurar tu token de Telegram.

Crea un archivo llamado .env en la carpeta raíz (ObligatorioBotAlgoritmos/) con este contenido:

TELEGRAM_TOKEN=tu_token_del_bot
API_URL=https://api.frankfurter.app


## El token del bot se obtiene desde @BotFather
 en Telegram.

## 5. Ejecutar el bot

Ejecutá el archivo principal:

python main.py


Si tu entorno virtual está activo, el bot se iniciará y se conectará automáticamente a Telegram.

## 6. Probar el bot

En Telegram, buscá tu bot (por ejemplo: @ElBotMarcelinhobot)
y escribí:

/start

Podrás acceder al menú principal y comenzar a interactuar con todas las funciones.

## 7. (Opcional) Ejecutar los tests o archivos de ejemplo

Tenés algunos archivos de prueba incluidos:

arbolTesting.xlsx → pruebas del árbol binario

mainTesting.xlsx → pruebas del flujo principal

transaccionesTesting.xlsx → simulaciones de transacciones

Podés abrirlos para ver ejemplos de entrada y salida de datos del sistema.

El bot estará activo y listo para usarse en Telegram.

## Cómo usarlo

Abre Telegram y busca el bot con el nombre @ElBotMarcelinhobot.

Inicia la conversación con /start.

Explora el menú principal para acceder a todas las funcionalidades.

Puedes escribir /menu en cualquier momento para volver al inicio.

## Mensajes de error comunes

Moneda no válida: El bot te pedirá que ingreses una moneda existente.

Fechas incorrectas: Debes usar el formato correcto (AAAA-MM-DD).

Conexión fallida: Verifica tu conexión a Internet o el estado de la API.

## Preguntas frecuentes

¿Cómo sé si mi transacción fue exitosa?
El bot te enviará un mensaje confirmando la operación.

¿Puedo reiniciar la sesión?
Sí, escribiendo /start o /menu.

## Autor
Rodrigo Correa

Correo Electronico: rodrigocorreamuse@gmail.com

Mi perfil en LinkedIn: https://www.linkedin.com/in/rodrigo-correa-b868b1368/

