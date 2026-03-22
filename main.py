import os
import requests
from dotenv import load_dotenv

# Lee el archivo .env
load_dotenv()

def ejecutar_logica_martech(ciudad):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad},pe&appid={api_key}&units=metric"
    
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        
        # SI LA API DA ERROR (Ej: llave no activa o mal escrita)
        if respuesta.status_code != 200:
            return f"Error de la API: {datos.get('message', 'Llave no activada aun')}"

        # SI LA API FUNCIONA, buscamos la temperatura
        temperatura = datos['main']['temp']
            
        # EN LUGAR DE UN STRING, DEVOLVEMOS UN DICCIONARIO
        return {
            "status": "ok",
            "ciudad": ciudad,
            "temperatura": temperatura,
        }

    except Exception as e:
        return f"Error técnico en el código: {e}"

def obtener_estrategia_marketing(temperatura):
    # Definimos los "Umbrales" de negocio
    if temperatura < 18:
        categoria = "FRIOLENTO"
        producto = "Seguro contra Influenza / Préstamo para Calefacción 🧤"
        color_hex = "#3498db" # Azul
    elif 18 <= temperatura <= 25:
        categoria = "TEMPLADO"
        producto = "Crédito de Consumo - ¡Renueva tu clóset! 👕"
        color_hex = "#2ecc71" # Verde
    else:
        categoria = "CALUROSO"
        producto = "Seguro de Viajes / Crédito Vehicular AC ☀️"
        color_hex = "#e67e22" # Naranja
        
    return {
        "segmento": categoria,
        "oferta_principal": producto,
        "color_interfaz": color_hex
    }
    
if __name__ == "__main__":
    # Pedimos al usuario que ingrese una ciudad
    ciudad = input("Ingrese el nombre de una ciudad en Perú: ")
    resultado = ejecutar_logica_martech(ciudad)

    # Si la respuesta es un error, lo mostramos
    if isinstance(resultado, str):
        print(resultado)
    # Si la respuesta es un diccionario, seguimos con la lógica de marketing
    else:
        print(f"Temperatura actual en {resultado['ciudad']}: {resultado['temperatura']}°C")
        estrategia = obtener_estrategia_marketing(resultado['temperatura'])
        print(f"Segmento: {estrategia['segmento']}")
        print(f"Oferta Principal: {estrategia['oferta_principal']}")
        print(f"Color recomendado para la interfaz: {estrategia['color_interfaz']}")