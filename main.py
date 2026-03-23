import os
import requests
import csv
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
    # 1. Definimos nuestro "Target" (Las ciudades donde tenemos clientes)
    ciudades_bcp = ["Lima", "Cusco", "Piura", "Arequipa", "Iquitos"]
    
    # 2. Creamos un contenedor para los resultados de la campaña
    reporte_final = []

    print("🚀 Iniciando procesamiento de campaña regional...\n")

    for ciudad in ciudades_bcp:
        # Reutilizamos tu función de API
        datos_clima = ejecutar_logica_martech(ciudad)

        if datos_clima["status"] == "ok":
            temp = datos_clima["temperatura"]
            # Reutilizamos tu lógica de negocio
            estrategia = obtener_estrategia_marketing(temp)
            
            # Guardamos la info estructurada
            resultado = {
                "Ciudad": ciudad,
                "Temperatura": temp,
                "Segmento": estrategia["segmento"],
                "Oferta": estrategia["oferta_principal"]
            }
            reporte_final.append(resultado)
            print(f"✅ Procesado: {ciudad} ({temp}°C) -> {estrategia['segmento']}")
        else:
            print(f"❌ Error en {ciudad}: {datos_clima['mensaje']}")

    # 3. Resumen Ejecutivo (Lo que le enviarías a tu jefe)
    print("\n" + "="*50)
    print("📊 RESUMEN DE CAMPAÑA - ACCIONES DISPONIBLES")
    print("="*50)
    for item in reporte_final:
        print(f"📍 {item['Ciudad']}: Enviar '{item['Oferta']}'")
    
    # --- 2. CREACIÓN DEL ARCHIVO CSV ---
    nombre_archivo = "campaña_clima_bcp.csv"
    columnas = ["Ciudad", "Temperatura", "Segmento", "Oferta"]

    try:
        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
            # Creamos el escritor de CSV basado en diccionarios
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            
            # Escribimos el encabezado (la primera fila)
            escritor.writeheader()
            
            # Escribimos todas las filas de nuestro reporte
            escritor.writerows(reporte_final)
            
        print(f"\n✅ ¡Éxito! Se ha generado el archivo: {nombre_archivo}")
        print(f"📂 Ubicación: {os.getcwd()}")
        
    except Exception as e:
        print(f"❌ Error al guardar el CSV: {e}")