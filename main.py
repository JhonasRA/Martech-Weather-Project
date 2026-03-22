import os
import requests
from dotenv import load_dotenv

# Lee el archivo .env
load_dotenv()

def ejecutar_logica_martech(ciudad="Lima"):
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
        
        if temperatura < 18:
            oferta = "Seguro de Salud - Plan Invierno ❄️"
        else:
            oferta = "Crédito Vehicular - Promoción Verano ☀️"
            
        return f"Dato: {ciudad} a {temperatura}°C. Acción: Ofrecer {oferta}"

    except Exception as e:
        return f"Error técnico en el código: {e}"

if __name__ == "__main__":
    print(ejecutar_logica_martech())